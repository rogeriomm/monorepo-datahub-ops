import pyspark
import rich
import sys, os
import subprocess
import squid
from squid.spark.session import get_spark
from common import show_spark_config, sql, run

sc, spark = get_spark(data_format = "iceberg")

spark.sparkContext.setLogLevel("ERROR")

show_spark_config(spark, [
    "spark.sql.extensions",
    "spark.sql.warehouse.dir",
    "spark.sql.shuffle.partitions",
    "spark.sql.catalog.spark_catalog",

    "spark.sql.catalog.local",
    "spark.sql.catalog.local.type",
    "spark.sql.catalog.local.warehouse",
    #"spark.sql.catalog.local.uri",
    #"spark.sql.catalog.iceberg",
])



print(f"{spark.sparkContext.uiWebUrl}")

spark.sql("CREATE NAMESPACE IF NOT EXISTS local.default")
spark.sql("USE local.default")

sql(spark, "SHOW NAMESPACES")
sql(spark, "SHOW CATALOGS")
sql(spark, "SHOW DATABASES")
sql(spark, "SHOW TABLES")

spark.stop()

