#
# https://github.com/134130/intellij-mise/issues/514
# Open Settings → Python → Debugger. Change Debugger mode from debugpy to pydevd.
# PyCharm 2026.2 also made debugpy the default debugger (JetBrains). https://blog.jetbrains.com/pycharm/2026/07/what-s-new-in-pycharm-2026-2/
#
# java -XshowSettings:properties -version 2>&1 | grep 'java.home'
#
import pyspark
import rich
import sys, os
import subprocess
import squid
from squid.spark.session import get_spark
from ingest import ingest
from common import show_spark_config, sql, run

run("echo $HOME")
run("echo $PATH")
print(f"Current directory: {os.getcwd()}")
#run("which java")

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

df = ingest(spark)

df.cache()

# Validate.
print(f"Records: {df.count():,}")
print(f"Columns: {len(df.columns)}")

df.createOrReplaceTempView("property_master_temp")
df.printSchema()
df.show(truncate=False)

sql(spark, "SELECT COUNT(*) FROM property_master_temp")

# Save as a managed Iceberg table.
table_name = "nyc_property_master"

spark.sql("CREATE NAMESPACE IF NOT EXISTS local.default")
spark.sql("USE local.default")

(
    df.writeTo(table_name)
    .using("iceberg")
    .createOrReplace()
)

sql(spark, "DESCRIBE TABLE local.default.nyc_property_master.files")

sql(spark, """ SELECT record_count, file_size_in_bytes, content_size_in_bytes, file_format, *
--   | Catalog | Namespace table | Iceberg metadata table |
FROM local.default.nyc_property_master.files """)

sql(spark, "SHOW NAMESPACES")
sql(spark, "SHOW CATALOGS")
sql(spark, "SHOW DATABASES")
sql(spark, "SHOW TABLES")

print("END")

spark.stop()
