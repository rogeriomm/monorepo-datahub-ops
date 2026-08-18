import os
from pathlib import Path
import subprocess

from squid.constants import (
    Environment,
    POSTGRES_ENDPOINTS,
    PostgresEndpoint,
    CERTIFICATE_DIR
)

def is_databricks() -> bool:
    return env in {
        Environment.DATABRICKS_FREE,
        Environment.DATABRICKS_PREMIUM,
    }

def get_postgres_endpoint() -> PostgresEndpoint:
    return POSTGRES_ENDPOINTS[env]

def get_git_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())

def get_chroot_volumes(path: Path, base: str | None) -> Path | None:

    match env:
        case Environment.DEBUG:
            path = repo_path / "on-premises/docker" / path.relative_to("/")


    if base is not None:
        path = path / Path(base)

    return path


def _is_databricks() -> bool:
    return "DATABRICKS_RUNTIME_VERSION" in os.environ

def _detect_environment() -> Environment:
    if _is_databricks():
        return Environment.DATABRICKS_FREE

    # TODO Environment.DATABRICKS_PREMIUM

    if Path("/Volumes").is_dir():
        # Running inside Docker container
        return Environment.ON_PREMISES

    # Running locally in an IDE/debug environment
    return Environment.DEBUG

# Detect environment: Databricks Free Edition/Premium, on premises, debug ...
env = _detect_environment()
repo_path: Path | None = None

if env == Environment.DEBUG:
    repo_path = get_git_root()
