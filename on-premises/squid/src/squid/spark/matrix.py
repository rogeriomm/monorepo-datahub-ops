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
        "delta": {
            "version": "4.4.0",
            "package": "io.delta:delta-spark_4.2_2.13:4.4.0",
            "extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "catalog_name": "local",
            "catalog_id": 1,
            "catalog": {
                "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            },
        },
        # Apache Iceberg does not yet publish a Spark 4.2
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
