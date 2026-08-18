from pyspark.sql import SparkSession
import squid.resources.postgres

spark = (
    SparkSession.builder
    .appName("test")
    .config(
        "spark.jars.packages",
        "org.postgresql:postgresql:42.7.9",
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    squid.resources.postgres.postgres_options(spark.read)
    .option("query", "SELECT version()")
    .load()
)

df.show(truncate=False)






