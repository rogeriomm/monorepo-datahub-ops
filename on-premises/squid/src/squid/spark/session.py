import findspark

import squid.core.main
from squid.constants import Environment

findspark.init()    

from pyspark import SparkConf, SparkContext
import pyspark

from typing import Tuple, Any
from pyspark.sql import SparkSession
from pyspark import SparkContext

from pathlib import Path

import os
import shutil
import socket
import hashlib
import tempfile
from html import escape
from types import MethodType
from urllib.request import urlopen

#
# https://docs.delta.io/releases/
# https://iceberg.apache.org/docs/latest/spark-getting-started/
spark_matrix = {
    "4.2": {
        "scala": "2.13",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.5.0",
            "package": "org.apache.hadoop:hadoop-aws:3.5.0",
        },
        "avro": {
            "version": "4.2.0",
            "package": "org.apache.spark:spark-avro_2.13:4.2.0",
        },
        "kafka": {
            "version": "4.2.0",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0",
        },
    },
    "4.1": {
        "scala": "2.13",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.4.2",
            "package": "org.apache.hadoop:hadoop-aws:3.4.2",
        },
        "avro": {
            "version": "4.1.3",
            "package": "org.apache.spark:spark-avro_2.13:4.1.3",
        },
        "kafka": {
            "version": "4.1.3",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.3",
        },
        "delta": {
            "version": "4.1.0",
            "package": "io.delta:delta-spark_4.1_2.13:4.1.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "local",
            "catalog_id": 1,
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.11.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-4.1_2.13:1.11.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog_name": "local",
            "catalog_id": 2,
            "catalog": {
                "spark.sql.catalog.local":
                    "org.apache.iceberg.spark.SparkCatalog",
                "spark.sql.catalog.local.type":
                    "hive",
            },
        },
    },
    "4.0": {
        "scala": "2.13",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.4.1",
            "package": "org.apache.hadoop:hadoop-aws:3.4.1",
        },
        "avro": {
            "version": "4.0.0",
            "package": "org.apache.spark:spark-avro_2.13:4.0.0",
        },
        "kafka": {
            "version": "4.0.0",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0",
        },
        "delta": {
            "version": "4.0.0",
            "package": "io.delta:delta-spark_2.13:4.0.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "local",
            "catalog_id": "1",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.11.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-4.0_2.13:1.11.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog_name": "local",
            "catalog_id": "2",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.5": {
        "scala": "2.12",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.3.4",
            "package": "org.apache.hadoop:hadoop-aws:3.3.4",
        },
        "avro": {
            "version": "3.5.9",
            "package": "org.apache.spark:spark-avro_2.12:3.5.9",
        },
        "kafka": {
            "version": "3.5.9",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.9",
        },
        "delta": {
            "version": "3.3.2",
            "package": "io.delta:delta-spark_2.12:3.3.2",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "local",
            "catalog_id": "1",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.11.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.11.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog_name": "local",
            "catalog_id": "2",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.4": {
        "scala": "2.12",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.3.4",
            "package": "org.apache.hadoop:hadoop-aws:3.3.4",
        },
        "avro": {
            "version": "3.4.0",
            "package": "org.apache.spark:spark-avro_2.12:3.4.0",
        },
        "kafka": {
            "version": "3.4.0",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0",
        },
        "delta": {
            "version": "2.4.0",
            "package": "io.delta:delta-core_2.12:2.4.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "local",
            "catalog_id": "1",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.4.3",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.4.3",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog_name": "local",
            "catalog_id": "2",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.3": {
        "scala": "2.12",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.3.2",
            "package": "org.apache.hadoop:hadoop-aws:3.3.2",
        },
        "avro": {
            "version": "3.3.0",
            "package": "org.apache.spark:spark-avro_2.12:3.3.0",
        },
        "kafka": {
            "version": "3.3.0",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0",
        },
        "delta": {
            "version": "2.3.0",
            "package": "io.delta:delta-core_2.12:2.3.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "spark_catalog",
            "catalog_id": "1",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.3.1",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.1",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog_name": "spark_catalog",
            "catalog_id": "2",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.2": {
        "scala": "2.12",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.3.1",
            "package": "org.apache.hadoop:hadoop-aws:3.3.1",
        },
        "avro": {
            "version": "3.2.0",
            "package": "org.apache.spark:spark-avro_2.12:3.2.0",
        },
        "kafka": {
            "version": "3.2.0",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0",
        },
        "delta": {
            "version": "2.0.2",
            "package": "io.delta:delta-core_2.12:2.0.2",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "spark_catalog",
            "catalog_id": "1",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.1.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:1.1.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog_name": "spark_catalog",
            "catalog_id": "2",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.1": {
        "scala": "2.12",
        "postgres": {
            "version": "42.7.7",
            "package": "org.postgresql:postgresql:42.7.7",
        },
        "trino": {
            "version": "483",
            "package": "io.trino:trino-jdbc:483",
        },
        "s3": {
            "version": "3.2.0",
            "package": "org.apache.hadoop:hadoop-aws:3.2.0",
        },
        "avro": {
            "version": "3.1.0",
            "package": "org.apache.spark:spark-avro_2.12:3.1.0",
        },
        "kafka": {
            "version": "3.1.0",
            "package": "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.0",
        },
        "delta": {
            "version": "1.0.1",
            "package": "io.delta:delta-core_2.12:1.0.1",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "spark_catalog",
            "catalog_id": "1",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "0.14.1",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.1_2.12:0.14.1",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog_name": "spark_catalog",
            "catalog_id": "2",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
}

def get_spark_major_minor_version() -> str:
    version_parts = pyspark.__version__.split(".")
    return ".".join(version_parts[:2])


def get_spark_packages(
    spark_version: str | None = None,
    data_format: str | None = None,
) -> str:
    spark_version = spark_version or get_spark_major_minor_version()
    matrix = spark_matrix[spark_version]
    data_format = _normalize_data_format(data_format)
    packages = [
        matrix["postgres"]["package"],
        #matrix["trino"]["package"], # FIXME: BAD
        matrix["s3"]["package"],
        matrix["avro"]["package"],
        matrix["kafka"]["package"]
    ]

    if data_format is None:
        return ",".join(packages)

    format_config = matrix.get(data_format)
    if format_config is None:
        raise ValueError(f"{data_format} is not supported for Spark {spark_version}")

    packages.append(format_config["package"])
    return ",".join(packages)


def get_spark_sql_extensions(
    spark_version: str | None = None,
    data_format: str | None = None,
) -> str:
    spark_version = spark_version or get_spark_major_minor_version()
    matrix = spark_matrix[spark_version]
    data_format = _normalize_data_format(data_format)

    if data_format is None:
        return ""

    format_config = matrix.get(data_format.lower())
    if format_config is None:
        raise ValueError(f"{data_format} is not supported for Spark {spark_version}")

    return format_config["extensions"]


def get_spark_catalog_configs(
    spark_version: str | None = None,
    data_format: str | None = None,
) -> tuple[dict[str, str], int]:
    spark_version = spark_version or get_spark_major_minor_version()
    matrix = spark_matrix[spark_version]
    data_format = _normalize_data_format(data_format)

    if data_format is None:
        return {}, 0

    format_config = matrix.get(data_format.lower())
    if format_config is None:
        raise ValueError(f"{data_format} is not supported for Spark {spark_version}")

    catalog_configs = dict(format_config.get("catalog", {}))

    # Configure the registered catalog (older matrix entries call it "local"
    # even though they register spark_catalog).
    for catalog_key in tuple(catalog_configs):
        if catalog_key.count(".") == 3:
            catalog_configs[f"{catalog_key}.warehouse"] = "s3a://trino-lakehouse"
            if data_format == "iceberg":
                catalog_configs[f"{catalog_key}.uri"] = _get_hive_metastore_uri()

    catalog_id = int(format_config["catalog_id"])

    return catalog_configs, catalog_id


def _normalize_data_format(data_format: str | None) -> str | None:
    if data_format is None:
        return None

    normalized = data_format.strip().lower()
    if normalized in {"", "none"}:
        return None

    if normalized not in {"delta", "iceberg"}:
        raise ValueError("data_format must be one of: None, Delta, Iceberg")

    return normalized


def _get_jupyter_service_name() -> str:
    service_name = (
        os.environ.get("JUPYTER_SERVICE_NAME")
        or os.environ.get("COMPOSE_SERVICE_NAME")
        or os.environ.get("HOSTNAME")
        or socket.gethostname()
    )

    return service_name.replace(" ", "-").lower()


def _get_jupyter_service_host(service_name: str) -> str:
    return service_name.replace(".", "-").replace(" ", "-").lower()


def _get_traefik_http_port() -> str:
    return os.environ.get("TRAEFIK_HTTP_PORT", "8080")


def _get_spark_ui_proxy_url(service_name: str) -> str:
    return (
        f"http://{_get_jupyter_service_host(service_name)}.localhost:"
        f"{_get_traefik_http_port()}/webui/"
    )


def _patch_spark_context_repr(spark_context: SparkContext, spark_ui_url: str) -> None:
    def _repr_html_override(self: SparkContext) -> str:
        return """
<div>
  <div style="font-weight: 600; margin-bottom: 0.5rem;">SparkContext</div>
  <div style="margin-bottom: 0.75rem;">
    <a href="{spark_ui_url}" target="_blank" rel="noopener noreferrer">Spark UI</a>
  </div>
  <table>
    <tr><th align="left">Version</th><td>{version}</td></tr>
    <tr><th align="left">Master</th><td>{master}</td></tr>
    <tr><th align="left">AppName</th><td>{app_name}</td></tr>
  </table>
</div>
""".format(
            spark_ui_url=escape(spark_ui_url, quote=True),
            version=escape(self.version),
            master=escape(self.master),
            app_name=escape(self.appName),
        )

    spark_context._repr_html_ = MethodType(_repr_html_override, spark_context)


def _get_hive_metastore_uri() -> str:
    return os.environ.get("HIVE_METASTORE_URI") or "thrift://hive-metastore:9083"


def _resolve_iceberg_hive_client_jars(spark_version: str) -> list[Path]:
    # Iceberg loads its Hive client from the driver classpath, independently
    # of Spark's isolated Hive client. Hive 2.3 uses RPCs removed in Hive 4.
    jars = [
        _cache_hive_client_jar(
            "org/apache/hive/hive-standalone-metastore-common/4.0.1/"
            "hive-standalone-metastore-common-4.0.1.jar",
            "f74d06e29a18d6a6b215b4e7b0445ef5c8bf7c73d5be4ab7eaed3f185cf000f8",
        )
    ]
    if int(spark_version.split(".")[0]) < 4:
        # Spark 3 bundles Thrift 0.12, which lacks the transport classes used
        # by the Hive 4 client. Spark 4 already supplies Thrift 0.16.
        jars.append(
            _cache_hive_client_jar(
                "org/apache/thrift/libthrift/0.16.0/libthrift-0.16.0.jar",
                "b311ad08f7dc5ba90139910ec8619460914a4a2952f738603f1d7803ffdbe0a8",
            )
        )
    return jars


def _cache_hive_client_jar(artifact_path: str, expected_sha256: str) -> Path:
    jar_name = artifact_path.rsplit("/", 1)[-1]
    cache_dir = Path.home() / ".cache" / "squid" / "hive-client"
    jar_path = cache_dir / jar_name
    if (
        jar_path.is_file()
        and hashlib.sha256(jar_path.read_bytes()).hexdigest() == expected_sha256
    ):
        return jar_path

    cache_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://repo.maven.apache.org/maven2/{artifact_path}"
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=cache_dir, delete=False) as temporary:
            temporary_path = Path(temporary.name)
            with urlopen(url, timeout=60) as response:
                shutil.copyfileobj(response, temporary)
        if hashlib.sha256(temporary_path.read_bytes()).hexdigest() != expected_sha256:
            raise RuntimeError(f"Checksum mismatch for {jar_name}")
        temporary_path.replace(jar_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return jar_path


def _configure_spark_java() -> None:
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        java_home_path = Path(java_home).expanduser().resolve()
        if (java_home_path / "bin" / "java").is_file():
            os.environ["JAVA_HOME"] = str(java_home_path)
            return

    java_executable = shutil.which("java")
    if java_executable is None:
        raise FileNotFoundError("Java executable not found via JAVA_HOME or PATH")

    java_path = Path(java_executable).resolve()
    if not java_path.is_file():
        raise FileNotFoundError(f"Java executable not found: {java_path}")

    os.environ["JAVA_HOME"] = str(java_path.parent.parent)



def iter_spark_jar_dirs() -> list[Path]:
    candidates = []

    spark_home = os.environ.get("SPARK_HOME")
    if spark_home:
        candidates.append(Path(spark_home) / "jars")

    candidates.append(Path(pyspark.__file__).resolve().parent / "jars")
    return [path for path in candidates if path.exists()]


def resolve_listener_jar(sparkmonitor_dir: Path) -> Path:
    for jars_dir in iter_spark_jar_dirs():
        for jar in jars_dir.glob("spark-core_*.jar"):
            # spark-core_2.13-3.5.8.jar => scala=2.13, spark_major=3
            scala_ver, spark_ver = jar.name.split("_")[1].split("-")[:2]
            spark_major = spark_ver.split(".")[0]
            if spark_major == "3" and scala_ver == "2.12":
                return sparkmonitor_dir / "listener_spark3_2.12.jar"
            if spark_major == "3" and scala_ver == "2.13":
                return sparkmonitor_dir / "listener_spark3_2.13.jar"
            if spark_major == "4" and scala_ver == "2.13":
                return sparkmonitor_dir / "listener_spark4_2.13.jar"

    raise RuntimeError(
        "Could not detect Spark/Scala version from SPARK_HOME or the pyspark installation"
    )


#
# https://docs.delta.io/quick-start/
#   bin/spark-sql --packages io.delta:delta-spark_2.13:4.0.0 \
#        --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
#        --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"
#
def get_spark(
    port_offset: int | None = None,
    driver_memory: str = "16g",
    executor_memory: str = "8g",
    data_format: str | None = None,
    profile: str | None = None
) -> Tuple[SparkContext, SparkSession]:
    _configure_spark_java()
    spark_version = get_spark_major_minor_version()
    data_format = _normalize_data_format(data_format)
    service_name = _get_jupyter_service_name()
    print(
        "Spark version: "
        f"{pyspark.__version__}, Driver memory: {driver_memory}, "
        f"Executor memory: {executor_memory}, Service: {service_name}, "
        f"Data format: {data_format}"
    )
    spark_packages = get_spark_packages(spark_version, data_format)
    spark_sql_extensions = get_spark_sql_extensions(spark_version, data_format)
    spark_catalog_configs, catalog_id = get_spark_catalog_configs(spark_version, data_format)
    spark_ui_proxy_url = _get_spark_ui_proxy_url(service_name)
    driver_classpath = []
    if data_format == "iceberg":
        driver_classpath.extend(
            str(jar) for jar in _resolve_iceberg_hive_client_jars(spark_version)
        )

    if port_offset is None:
        port_offset = catalog_id + 1

    print(f"Port offset: {port_offset}")

    print(f"Spark packages: {spark_packages}")
    print(f"Spark extensions: {spark_sql_extensions}")
    print(f"Spark catalog configs: {spark_catalog_configs}")

    builder = (
        SparkSession.builder
        .appName("main")
        .master("local[12]")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.port", str(7077 + port_offset))
        .config("spark.blockManager.port", str(7078 + port_offset))
        .config("spark.ui.port", str(4040 + port_offset))
        .config("spark.ui.bindAddress", "0.0.0.0")
        .config("spark.port.maxRetries", "0")
        .config("spark.driver.memory", driver_memory)
        .config("spark.executor.memory", executor_memory)

        .config("spark.sql.warehouse.dir", "s3a://trino-lakehouse")
        # Use Spark's supported client shim rather than its bundled Hive 2.3
        # client. The metastore server remains the Compose Hive 4.2 service.
        .config(
            "spark.sql.hive.metastore.version",
            "4.0.1" if int(spark_version.split(".")[0]) >= 4 else "3.1.3",
        )
        .config("spark.sql.hive.metastore.jars", "maven")
        .config(
            "spark.hadoop.hive.metastore.uris",
            _get_hive_metastore_uri(),
        )
        .enableHiveSupport()            

        # AWS S3
        .config("spark.hadoop.fs.s3a.impl",                      "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.experimental.fadvise",      "random")
        .config("spark.hadoop.fs.s3a.endpoint",                  "https://s3.amazonaws.com")
        .config(
               "spark.hadoop.fs.s3a.aws.credentials.provider",
               "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider"
        )

        .config("spark.hadoop.fs.s3a.access.key",      os.environ.get("AWS_ACCESS_KEY_ID", ""))
        .config("spark.hadoop.fs.s3a.secret.key",      os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
        .config("spark.hadoop.fs.s3a.session.token",   os.environ.get("AWS_SESSION_TOKEN", ""))
        .config("spark.hadoop.fs.s3a.endpoint.region", os.environ.get("AWS_REGION", "us-east-1"))
    )

    # The shared Hive warehouse lives in SeaweedFS. Bucket overrides keep
    # native AWS credentials and endpoints available for other S3 buckets.
    warehouse_s3_configs = {
        "endpoint": "http://seaweedfs:8334",
        "endpoint.region": "us-east-1",
        "path.style.access": "true",
        "connection.ssl.enabled": "false",
        "aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        "access.key": os.environ["SEAWEEDFS_ACCESS_KEY_ID"],
        "secret.key": os.environ["SEAWEEDFS_SECRET_ACCESS_KEY"],
    }
    for config_name, config_value in warehouse_s3_configs.items():
        builder = builder.config(
            f"spark.hadoop.fs.s3a.bucket.trino-lakehouse.{config_name}", config_value
        )
    if squid.core.main.env != Environment.DEBUG:
        import sparkmonitor

        sparkmonitor_dir = Path(sparkmonitor.__file__).resolve().parent
        listener_jar = resolve_listener_jar(sparkmonitor_dir)
        driver_classpath.append(str(listener_jar))
        builder = (
            builder
            .config("spark.ui.proxyRedirectUri", spark_ui_proxy_url)
            # https://github.com/swan-cern/sparkmonitor#example-with-a-manually-specified-listener-jar-path
            .config(
                "spark.extraListeners",
                "sparkmonitor.listener.JupyterSparkMonitorListener",
            )
        )

    if driver_classpath:
        builder = builder.config(
            "spark.driver.extraClassPath", os.pathsep.join(driver_classpath)
        )

    if spark_packages:
        builder = builder.config("spark.jars.packages", spark_packages)

    if spark_sql_extensions:
        builder = builder.config("spark.sql.extensions", spark_sql_extensions)

    for config_name, config_value in spark_catalog_configs.items():
        builder = builder.config(config_name, config_value)

    spark_session: SparkSession = builder.getOrCreate()

    spark_context: SparkContext = spark_session.sparkContext
    _patch_spark_context_repr(spark_context, spark_ui_proxy_url)

    return spark_context, spark_session
