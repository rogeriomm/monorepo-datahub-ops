"""Read messages from the ``my-topic`` Kafka topic with PySpark.

Run inside the ``jupyter-spark-4.1`` container:

    spark-submit \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.3 \
      /home/jovyan/work/notebooks/jupyter/kafka/kafka-read-stream.py

Produce messages from ``kafka-hello-world-kafkactl.ipynb`` and they will be
printed to this process's console.
"""

import os

from pyspark.sql import SparkSession


bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-4-backend:29092")
topic = os.getenv("KAFKA_TOPIC", "my-topic")
truststore_location = os.getenv(
    "KAFKA_TRUSTSTORE_LOCATION",
    "/etc/kafka/tls/kafka.truststore.p12",
)
truststore_password = os.getenv("KAFKA_TRUSTSTORE_PASSWORD", "changeit")

spark = SparkSession.builder.appName("kafka-read-stream").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

messages = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", bootstrap_servers)
    .option("subscribe", topic)
    .option("startingOffsets", "earliest")
    .option("kafka.security.protocol", "SSL")
    .option("kafka.ssl.truststore.location", truststore_location)
    .option("kafka.ssl.truststore.password", truststore_password)
    .option("kafka.ssl.truststore.type", "PKCS12")
    .load()
    .selectExpr(
        "CAST(key AS STRING) AS key",
        "CAST(value AS STRING) AS value",
        "topic",
        "partition",
        "offset",
        "timestamp",
    )
)

query = (
    messages.writeStream.format("console")
    .outputMode("append")
    .option("truncate", "false")
    .start()
)

try:
    query.awaitTermination()
finally:
    query.stop()
    spark.stop()
