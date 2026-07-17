import findspark

findspark.init()    

from pyspark import SparkConf, SparkContext
import pyspark

from typing import Tuple
from pyspark.sql import SparkSession
from pyspark import SparkContext

from pathlib import Path

import os
import socket

#
# https://docs.delta.io/releases/
# https://iceberg.apache.org/docs/latest/spark-getting-started/
spark_matrix = {
    "4.1": {
        "scala": "2.13",
        "delta": {
            "version": "4.1.0",
            "package": "io.delta:delta-spark_4.1_2.13:4.1.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.11.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-4.1_2.13:1.11.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog": {
                "spark.sql.catalog.local":
                    "org.apache.iceberg.spark.SparkCatalog",
                "spark.sql.catalog.local.type":
                    "hadoop",
            },
        },
    },
    "4.0": {
        "scala": "2.13",
        "delta": {
            "version": "4.0.0",
            "package": "io.delta:delta-spark_2.13:4.0.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.11.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-4.0_2.13:1.11.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.5": {
        "scala": "2.12",
        "delta": {
            "version": "3.3.2",
            "package": "io.delta:delta-spark_2.12:3.3.2",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.11.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.11.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.4": {
        "scala": "2.12",
        "delta": {
            "version": "2.4.0",
            "package": "io.delta:delta-core_2.12:2.4.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.4.3",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.4.3",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.3": {
        "scala": "2.12",
        "delta": {
            "version": "2.3.0",
            "package": "io.delta:delta-core_2.12:2.3.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.3.1",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.1",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.2": {
        "scala": "2.12",
        "delta": {
            "version": "2.0.2",
            "package": "io.delta:delta-core_2.12:2.0.2",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "1.1.0",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:1.1.0",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkSessionCatalog",
                "spark.sql.catalog.spark_catalog.type": "hive",
            },
        },
    },
    "3.1": {
        "scala": "2.12",
        "delta": {
            "version": "1.0.1",
            "package": "io.delta:delta-core_2.12:1.0.1",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        "iceberg": {
            "version": "0.14.1",
            "package": "org.apache.iceberg:iceberg-spark-runtime-3.1_2.12:0.14.1",
            "extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
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

    if data_format is None:
        return ""

    format_config = matrix.get(data_format)
    if format_config is None:
        raise ValueError(f"{data_format} is not supported for Spark {spark_version}")

    return format_config["package"]


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
) -> dict[str, str]:
    spark_version = spark_version or get_spark_major_minor_version()
    matrix = spark_matrix[spark_version]
    data_format = _normalize_data_format(data_format)

    if data_format is None:
        return {}

    format_config = matrix.get(data_format.lower())
    if format_config is None:
        raise ValueError(f"{data_format} is not supported for Spark {spark_version}")

    catalog_configs = dict(format_config.get("catalog", {}))

    if data_format == "iceberg" and spark_version == "4.1":
        catalog_configs["spark.sql.catalog.local.warehouse"] = (
            f"file://{_get_spark_warehouse_dir(spark_version, data_format)}"
        )

    return catalog_configs


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


def _get_spark_base_dir(
    service_name: str,
    spark_version: str,
    data_format: str | None,
) -> Path:
    return (
        Path.home()
        / "work"
        / "data"
        / "datalake"
        / service_name
        / f"spark-{spark_version}"
        / (data_format or "none")
    )


def _get_spark_warehouse_dir(
    spark_version: str,
    data_format: str | None,
) -> Path:
    return _get_spark_base_dir(_get_jupyter_service_name(), spark_version, data_format) / "warehouse"

#
# https://docs.delta.io/quick-start/
#   bin/spark-sql --packages io.delta:delta-spark_2.13:4.0.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"
#
def get_spark(
    port_offset: int = 2,
    driver_memory: str = "16g",
    executor_memory: str = "8g",
    data_format: str | None = None,
) -> Tuple[SparkContext, SparkSession]:
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
    spark_catalog_configs = get_spark_catalog_configs(spark_version, data_format)

    print(f"Spark packages: {spark_packages}")
    print(f"Spark extensions: {spark_sql_extensions}")
    print(f"Spark catalog configs: {spark_catalog_configs}")

    base_dir = _get_spark_base_dir(service_name, spark_version, data_format)
    warehouse_dir = base_dir / "warehouse"
    metastore_db = base_dir / "metastore" / "metastore_db"
    derby_home = base_dir / "metastore" / "derby"

    builder = (
        SparkSession.builder
        .appName("main")
        .master("local[2]")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.port", str(7077 + port_offset))
        .config("spark.blockManager.port", str(7078 + port_offset))
        .config("spark.ui.port", str(4040 + port_offset))
        .config("spark.port.maxRetries", "0")
        .config("spark.driver.memory", driver_memory)
        .config("spark.executor.memory", executor_memory)
        ##.config("spark.driver.extraJavaOptions", "-Djava.net.preferIPv4Stack=true")
            
        .config("spark.sql.warehouse.dir", warehouse_dir)
        .config(
          "javax.jdo.option.ConnectionURL",
          f"jdbc:derby:{metastore_db};create=true"
        )
        .config(
           "spark.driver.extraJavaOptions",
            f"-Dderby.system.home={derby_home}"
        )            
        .enableHiveSupport()            

        # AWS S3
        #.config("spark.hadoop.fs.s3.impl",                       "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.impl",                      "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.experimental.fadvise",      "random")
        .config("spark.hadoop.fs.s3a.endpoint",                  "https://s3.amazonaws.com")
        #.config("spark.hadoop.fs.s3a.aws.credentials.provider",  "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider,com.amazonaws.auth.EnvironmentVariableCredentialsProvider,com.amazonaws.auth.InstanceProfileCredentialsProvider")
        .config(
               "spark.hadoop.fs.s3a.aws.credentials.provider",
               "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider"
        )
        #.config("spark.hadoop.fs.s3n.impl",                      "org.apache.hadoop.fs.s3native.NativeS3FileSystem")

        .config("spark.hadoop.fs.s3a.access.key",      os.environ["AWS_ACCESS_KEY_ID"])
        .config("spark.hadoop.fs.s3a.secret.key",      os.environ["AWS_SECRET_ACCESS_KEY"])
        .config("spark.hadoop.fs.s3a.session.token",   os.environ["AWS_SESSION_TOKEN"])        
        .config("spark.hadoop.fs.s3a.endpoint.region", os.environ.get("AWS_REGION", "us-east-1"))            
    )

    if spark_packages:
        builder = builder.config("spark.jars.packages", spark_packages)

    if spark_sql_extensions:
        builder = builder.config("spark.sql.extensions", spark_sql_extensions)

    for config_name, config_value in spark_catalog_configs.items():
        builder = builder.config(config_name, config_value)

    spark_session: SparkSession = builder.getOrCreate()

    spark_context: SparkContext = spark_session.sparkContext

    return spark_context, spark_session
