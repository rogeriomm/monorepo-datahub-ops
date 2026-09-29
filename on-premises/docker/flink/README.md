# Apache Flink with Kafka CDC and Iceberg

This image runs Apache Flink 2.1.3 with the Kafka SQL connector and Apache
Iceberg 1.11.0. It reads Debezium CDC events from Kafka and writes upserts and
deletes to Iceberg tables in the `trino-lakehouse` SeaweedFS S3 bucket. Flink
does not connect to PostgreSQL, and Delta Lake is no longer part of the image.

The Apache Flink CDC 3.6 pipeline API cannot be used for this path because its
Kafka pipeline connector is sink-only. Flink SQL provides the supported Kafka
source and interprets Debezium JSON as CDC changelog rows. Flink 2.1 is retained
because the released Kafka SQL connector and Iceberg runtime both support it;
Flink 2.3 does not yet have a released Kafka connector.

The complete data path is:

```text
PostgreSQL -> Debezium -> Kafka -> Flink SQL -> Iceberg -> SeaweedFS S3
```

Start PostgreSQL, Debezium, Kafka, SeaweedFS, and Flink:

```bash
docker compose --profile cdc --profile flink up -d --build
```

The default example reads `postgres.public.customers`, matching
`DEBEZIUM_TOPIC_PREFIX=postgres` and `DEBEZIUM_SCHEMA=public`. Before
submission, update the topic and columns in `kafka-debezium-to-iceberg.sql` to
match the source table. Every captured table must have a primary key.

Submit the replication job with:

```bash
docker compose exec flink-jobmanager \
  /opt/flink/bin/sql-client.sh \
  -f /opt/flink/examples/kafka-debezium-to-iceberg.sql
```

Open the Flink UI at <http://flink.localhost:8080> when
`TRAEFIK_HTTP_PORT` uses its default value.

The example creates a format-version 2 Iceberg table with upsert writes. Kafka
offsets and Iceberg commits are coordinated by Flink checkpoints. The table
uses an Iceberg Hadoop catalog at `s3://trino-lakehouse/flink-cdc`; its files
share SeaweedFS storage with the Trino lakehouse, but the table is not
automatically registered in the existing Trino Hive catalog.
