from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pyspark.sql import SparkSession
from pyspark.sql.readwriter import DataFrameReader

from squid.core.main import get_postgres_endpoint, is_databricks, get_chroot_volumes

from squid.constants import CERTIFICATE_DIR

from pyspark.sql.readwriter import DataFrameReader, DataFrameWriter

type DataFrameIO = DataFrameReader | DataFrameWriter

if TYPE_CHECKING:
    from databricks.sdk import WorkspaceClient
    from psycopg2.extensions import cursor as PostgresCursor


postgres_endpoint = get_postgres_endpoint()

postgres_database = "postgres"
postgres_user = "postgres"

scope = "on-premises-integration"

certificate_dir = get_chroot_volumes(CERTIFICATE_DIR, "postgres")

ca_certificate_path = certificate_dir / "ca.crt"
client_certificate_path = certificate_dir  / "client.crt"
client_key_path = certificate_dir / "client.key"
client_keystore_path = certificate_dir / "postgres-client.p12"

client_keystore_password: str | None = None
postgres_password: str | None = None

def _is_good() -> bool:
    """Return whether all PEM files required for a psycopg2 mTLS connection exist."""
    try:
        return all(
            certificate_path.is_file() and certificate_path.stat().st_size > 0
            for certificate_path in (
                ca_certificate_path,
                client_certificate_path,
                client_key_path,
            )
        )
    except OSError:
        return False


def _read_local_password() -> tuple[str | None, str | None] | tuple[None, None]:
    password_path = certificate_dir / "secret-postgres-password"

    try:
        password = password_path.read_text().strip()
    except FileNotFoundError:
        return None, None

    password_path = certificate_dir / "secret-client-password"

    try:
        client_password = password_path.read_text().strip()
    except FileNotFoundError:
        return None, None

    return client_password or None, password or None


def _load_databricks_secrets(
    workspace_client: WorkspaceClient | None,
) -> tuple[str | None, str | None]:
    from databricks.sdk import WorkspaceClient
    from databricks.sdk.errors import ResourceDoesNotExist

    client = workspace_client or WorkspaceClient()

    def get_optional_secret(key: str) -> str | None:
        try:
            return client.dbutils.secrets.get(scope=scope, key=key)
        except ResourceDoesNotExist:
            return None

    return (
        get_optional_secret("postgres-client-keystore-password"),
        get_optional_secret("postgres-password"),
    )


def get_cursor(
    workspace_client: WorkspaceClient | None = None,
) -> PostgresCursor | None:
    """Open an mTLS PostgreSQL connection and return a cursor for it."""
    global client_keystore_password
    global postgres_password

    if not _is_good():
        return None

    loaded_client_keystore_password: str | None = None
    loaded_postgres_password: str | None = None

    if is_databricks():
        (
            loaded_client_keystore_password,
            loaded_postgres_password,
        ) = _load_databricks_secrets(workspace_client)
    else:
        (
            loaded_client_keystore_password,
            loaded_postgres_password,
        ) = _read_local_password()

    try:
        import psycopg2
    except ImportError as error:
        raise RuntimeError(
            "psycopg2 is not installed; install psycopg2-binary"
        ) from error

    with tempfile.TemporaryDirectory(prefix="squid-postgres-") as temp_dir:
        temporary_dir = Path(temp_dir)
        temporary_ca = temporary_dir / "ca.crt"
        temporary_certificate = temporary_dir / "client.crt"
        temporary_key = temporary_dir / "client.key"

        for source, destination in (
            (ca_certificate_path, temporary_ca),
            (client_certificate_path, temporary_certificate),
            (client_key_path, temporary_key),
        ):
            shutil.copyfile(source, destination)
            destination.chmod(0o600)

        connection_params: dict[str, Any] = {
            "host": postgres_endpoint.hostname,
            "port": postgres_endpoint.port,
            "database": postgres_database,
            "user": postgres_user,
            "sslmode": "verify-full",
            "sslrootcert": str(temporary_ca),
            "sslcert": str(temporary_certificate),
            "sslkey": str(temporary_key),
        }
        if loaded_postgres_password is not None:
            connection_params["password"] = loaded_postgres_password

        connection = psycopg2.connect(**connection_params)
        try:
            cursor = connection.cursor()
        except Exception:
            connection.close()
            raise

    client_keystore_password = loaded_client_keystore_password
    postgres_password = loaded_postgres_password

    return cursor


def postgres_options(io: DataFrameIO) -> DataFrameIO:
    (
        _,
        loaded_postgres_password,
    ) = _read_local_password()
    global postgres_password

    postgres_password = loaded_postgres_password

    return (
        io
        .format("jdbc")
        .option("driver", "org.postgresql.Driver")
        .option("user", postgres_user)
        .option("password", postgres_password)
        .option("sslmode", "require")
        .option(
            "url",
            f"jdbc:postgresql://"
            f"{postgres_endpoint.hostname}:"
            f"{postgres_endpoint.port}/"
            f"{postgres_database}",
        )
    )

