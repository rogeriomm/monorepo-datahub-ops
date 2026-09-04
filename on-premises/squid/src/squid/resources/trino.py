from __future__ import annotations

import os
import ssl
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import requests
import trino
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    pkcs12,
)
from requests.adapters import HTTPAdapter
from trino.auth import CertificateAuthentication
from urllib3.util.ssl_ import create_urllib3_context

from squid.constants import CERTIFICATE_DIR, Environment
from squid.core.main import env, get_chroot_volumes, is_databricks

if TYPE_CHECKING:
    from databricks.sdk import WorkspaceClient
    from trino.dbapi import Cursor, Connection

scope = "on-premises-integration"

certificate_dir = get_chroot_volumes(CERTIFICATE_DIR, "trino")
ca_certificate_path = certificate_dir / "ca.crt"
client_keystore_path = certificate_dir / "trino-client.p12"


class _TrinoHTTPAdapter(HTTPAdapter):
    def __init__(self, ssl_context: ssl.SSLContext) -> None:
        self._ssl_context = ssl_context
        super().__init__()

    def init_poolmanager(
        self,
        connections: int,
        maxsize: int,
        block: bool = False,
        **pool_kwargs: Any,
    ) -> None:
        pool_kwargs["ssl_context"] = self._ssl_context
        super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

    def proxy_manager_for(self, proxy: str, **proxy_kwargs: Any) -> Any:
        proxy_kwargs["ssl_context"] = self._ssl_context
        return super().proxy_manager_for(proxy, **proxy_kwargs)


def _get_endpoint() -> tuple[str, int]:
    if is_databricks():
        return "pub.worldb.dedyn.io", 9003
    if env == Environment.ON_PREMISES:
        return "trino", 8443
    return "localhost", 8443


def _load_client_keystore_password(
    workspace_client: WorkspaceClient | None,
) -> bytes:
    if is_databricks():
        from databricks.sdk import WorkspaceClient

        client = workspace_client or WorkspaceClient()
        password = client.dbutils.secrets.get(
            scope=scope,
            key="trino-client-keystore-password",
        )
    else:
        password = (certificate_dir / "secret-client-password").read_text().strip()

    if not password:
        raise ValueError("The Trino client keystore password is empty")
    return password.encode()


def _prepare_trino_mtls(
    client_keystore_password: bytes,
) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
    private_key, client_certificate, _ = pkcs12.load_key_and_certificates(
        client_keystore_path.read_bytes(),
        client_keystore_password,
    )

    if private_key is None or client_certificate is None:
        raise ValueError("trino-client.p12 does not contain a client identity")

    temporary_dir = tempfile.TemporaryDirectory(prefix="squid-trino-mtls-")
    temporary_path = Path(temporary_dir.name)
    client_certificate_path = temporary_path / "client.crt"
    client_key_path = temporary_path / "client.key"

    try:
        client_certificate_path.write_bytes(
            client_certificate.public_bytes(Encoding.PEM)
        )
        client_key_path.write_bytes(
            private_key.private_bytes(
                Encoding.PEM,
                PrivateFormat.PKCS8,
                NoEncryption(),
            )
        )
        os.chmod(client_key_path, 0o600)
    except Exception:
        temporary_dir.cleanup()
        raise

    return temporary_dir, client_certificate_path, client_key_path


def _create_http_session() -> requests.Session:
    ssl_context = create_urllib3_context()
    # Python 3.13 enables strict X.509 verification by default. The existing
    # development CA predates that policy because its Basic Constraints
    # extension is not marked critical. Keep certificate and hostname
    # verification enabled, but use the pre-3.13 verification policy.
    ssl_context.verify_flags &= ~getattr(ssl, "VERIFY_X509_STRICT", 0)

    session = requests.Session()
    session.verify = str(ca_certificate_path)
    session.mount("https://", _TrinoHTTPAdapter(ssl_context))
    return session


def get_trino(workspace_client: WorkspaceClient | None = None) -> Connection:
    """Open an mTLS Trino connection and return a DB-API cursor."""
    host, port = _get_endpoint()
    client_keystore_password = _load_client_keystore_password(workspace_client)
    temporary_dir, client_certificate_path, client_key_path = _prepare_trino_mtls(
        client_keystore_password
    )

    try:
        connection = trino.dbapi.connect(
            host=host,
            port=port,
            user="trino-client",
            catalog="postgresql",
            schema="public",
            http_scheme="https",
            auth=CertificateAuthentication(
                str(client_certificate_path),
                str(client_key_path),
            ),
            verify=str(ca_certificate_path),
            http_session=_create_http_session(),
        )
        # The Trino client reads the PEM files for subsequent HTTP requests, so
        # keep their temporary directory alive for as long as the connection.
        connection._squid_temporary_directory = temporary_dir
        return connection
    except Exception:
        temporary_dir.cleanup()
        raise
