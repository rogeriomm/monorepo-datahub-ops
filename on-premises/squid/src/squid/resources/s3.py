from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import boto3
from botocore.client import BaseClient
from botocore.config import Config

from squid.constants import CERTIFICATE_DIR, Environment
from squid.core.main import env, get_chroot_volumes, is_databricks

if TYPE_CHECKING:
    from databricks.sdk import WorkspaceClient


SECRET_SCOPE = "on-premises-integration"
DEFAULT_REGION = "us-east-1"

certificate_dir = get_chroot_volumes(CERTIFICATE_DIR, "seaweedfs")
ca_certificate_path = certificate_dir / "ca.crt"


def _default_endpoint_url() -> str | None:
    if is_databricks():
        return "https://pub.worldb.dedyn.io:9001"
    if env == Environment.ON_PREMISES:
        return "https://seaweedfs:8333"
    if env == Environment.DEBUG:
        return "https://localhost:8333"
    return None


def _load_databricks_credentials(
    workspace_client: WorkspaceClient | None,
) -> tuple[str, str]:
    from databricks.sdk import WorkspaceClient

    client = workspace_client or WorkspaceClient()
    return (
        client.dbutils.secrets.get(scope=SECRET_SCOPE, key="seaweedfs-user"),
        client.dbutils.secrets.get(scope=SECRET_SCOPE, key="seaweedfs-password"),
    )


def _resolve_credentials(
    workspace_client: WorkspaceClient | None,
    aws_access_key_id: str | None,
    aws_secret_access_key: str | None,
    using_seaweedfs: bool,
) -> tuple[str | None, str | None]:
    if (aws_access_key_id is None) != (aws_secret_access_key is None):
        raise ValueError(
            "aws_access_key_id and aws_secret_access_key must be provided together"
        )

    if aws_access_key_id is not None and aws_secret_access_key is not None:
        return aws_access_key_id, aws_secret_access_key

    if is_databricks() and using_seaweedfs:
        return _load_databricks_credentials(workspace_client)

    if using_seaweedfs:
        access_key = os.getenv("SEAWEEDFS_ACCESS_KEY_ID")
        secret_key = os.getenv("SEAWEEDFS_SECRET_ACCESS_KEY")
        if not access_key or not secret_key:
            raise RuntimeError(
                "SeaweedFS credentials are unavailable; set "
                "SEAWEEDFS_ACCESS_KEY_ID and SEAWEEDFS_SECRET_ACCESS_KEY"
            )
        return access_key, secret_key

    # Native AWS and compatible cloud deployments use Boto3's standard
    # credential provider chain when explicit credentials are not supplied.
    return None, None


def get_s3(
    workspace_client: WorkspaceClient | None = None,
    *,
    endpoint_url: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    region_name: str | None = None,
    verify: bool | str | None = None,
) -> BaseClient:
    """Return an environment-aware Boto3 S3 client.

    Known local and Databricks environments connect to the project's
    SeaweedFS S3 endpoint. Other environments use native S3 configuration and
    Boto3's normal credential provider chain. Every setting can be overridden
    for an additional S3-compatible deployment.
    """
    default_endpoint_url = _default_endpoint_url()
    resolved_endpoint_url = (
        endpoint_url
        or os.getenv("SQUID_S3_ENDPOINT_URL")
        or default_endpoint_url
    )
    using_seaweedfs = (
        default_endpoint_url is not None
        and resolved_endpoint_url == default_endpoint_url
    )
    resolved_access_key, resolved_secret_key = _resolve_credentials(
        workspace_client,
        aws_access_key_id,
        aws_secret_access_key,
        using_seaweedfs,
    )

    resolved_region_name = region_name or os.getenv("SQUID_S3_REGION")
    if resolved_region_name is None and using_seaweedfs:
        resolved_region_name = DEFAULT_REGION

    client_options: dict[str, Any] = {}
    if resolved_region_name is not None:
        client_options["region_name"] = resolved_region_name

    if resolved_endpoint_url is not None:
        client_options["endpoint_url"] = resolved_endpoint_url
        client_options["config"] = Config(s3={"addressing_style": "path"})
        if verify is not None:
            client_options["verify"] = verify
        elif using_seaweedfs:
            # The current public tunnel presents a certificate for the
            # internal SeaweedFS names. Match the existing Databricks
            # workaround until that endpoint has a matching certificate.
            client_options["verify"] = (
                False if is_databricks() else str(ca_certificate_path)
            )
    elif verify is not None:
        client_options["verify"] = verify

    if resolved_access_key is not None and resolved_secret_key is not None:
        client_options.update(
            {
                "aws_access_key_id": resolved_access_key,
                "aws_secret_access_key": resolved_secret_key,
            }
        )

    return boto3.client("s3", **client_options)
