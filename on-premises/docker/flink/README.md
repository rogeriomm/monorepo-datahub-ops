# Apache Flink with Delta Lake

This image runs Apache Flink 2.1.3 with the experimental Delta Lake 4.4.0
sink and the Apache Kafka SQL connector. It is configured to consume Debezium
JSON events from the Compose Kafka broker and store Delta tables in the
`delta-lakehouse` SeaweedFS S3 bucket.

The image applies `delta-seaweedfs.patch` to use path-style S3 addressing.
Delta 4.4.0 otherwise hardcodes virtual-host addressing after loading Hadoop
configuration, which is incompatible with the local SeaweedFS endpoint.

Start the integrated services:

```bash
docker compose --profile flink up -d \
  kafka-4 seaweedfs seaweedfs-init traefik flink-jobmanager flink-taskmanager
```

Open the Flink UI at <http://flink.localhost:8080> when
`TRAEFIK_HTTP_PORT` uses its default value.

The example in `kafka-debezium-to-delta.sql` shows an upsert pipeline. Update
its topic and schema, then submit it with:

```bash
docker compose exec flink-jobmanager \
  /opt/flink/bin/sql-client.sh -f /opt/flink/examples/kafka-debezium-to-delta.sql
```

The Delta connector is sink-only. Its upsert mode maps Debezium/Flink
`INSERT`, `UPDATE_AFTER`, and `DELETE` records to Delta Lake changes by the
declared primary key. Checkpointing controls when exactly-once Delta commits
become visible.
