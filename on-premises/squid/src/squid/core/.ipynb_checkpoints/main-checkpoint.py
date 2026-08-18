import os
from enum import Flag, Enum, auto
from pathlib import Path


class Environment(Enum):
    NONE = 1
    DATABRICKS_FREE = 2
    DATABRICKS_PREMIUM = 3
    ON_PREMISES = 5
    DEBUG = 6
    AWS = 7
    AZURE = 8
    GOOGLE = 9


def is_databricks() -> bool:
    return "DATABRICKS_RUNTIME_VERSION" in os.environ


def get_environment() -> Environment:
    if is_databricks():
       return Environment.DATABRICKS_FREE
    elif Path("/Volume").is_dir():
        return Environment.ON_PREMISES
    return Environment.DEBUG

