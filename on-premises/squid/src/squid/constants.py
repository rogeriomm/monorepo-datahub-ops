from enum import Enum, auto
from typing import NamedTuple
from pathlib import Path

class StorageConfig(NamedTuple):
    chroot: str

class PostgresEndpoint(NamedTuple):
    hostname: str
    port: int

class Environment(Enum):
    NONE = auto()
    DATABRICKS_FREE = auto()
    DATABRICKS_PREMIUM = auto()
    ON_PREMISES = auto()
    DEBUG = auto()
    AWS = auto()
    AZURE = auto()
    GOOGLE = auto()

STORAGE_CONFIG: dict[Environment, StorageConfig] = {
    # Databricks volumes
    Environment.DATABRICKS_FREE: StorageConfig(""),
    # Databricks volumes
    Environment.DATABRICKS_PREMIUM: StorageConfig(""),
    # Inside Docker container. See the docker-compose.yml
    Environment.ON_PREMISES: StorageConfig(""),
    # Debug. Host computer, git repository path
    Environment.DEBUG: StorageConfig("on-premises/docker/"),
}

CERTIFICATE_DIR = Path("/Volumes/workspace/default/on_premises_certificates")

POSTGRES_ENDPOINTS: dict[Environment, PostgresEndpoint] = {
    # Public Internet
    Environment.DATABRICKS_FREE: PostgresEndpoint("pub.worldb.dedyn.io", 900),
    # Public Internet
    Environment.DATABRICKS_PREMIUM: PostgresEndpoint("pub.worldb.dedyn.io", 900),
    # Inside Docker container.  See the docker-compose.yml
    Environment.ON_PREMISES: PostgresEndpoint("postgres", 5432),
    # Host running the Docker container. See the docker-compose.yml
    Environment.DEBUG: PostgresEndpoint("localhost", 5432),
}

