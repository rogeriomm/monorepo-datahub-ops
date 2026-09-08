# PostgreSQL CDC to Kafka

The `postgres` and `cdc` Compose profiles start PostgreSQL, Kafka, and Debezium
3.3.2.Final. The `trino` profile can still use PostgreSQL independently. Debezium
snapshots existing tables in `POSTGRES_DB` / `DEBEZIUM_SCHEMA` (defaults:
`postgres` / `public`), then streams committed changes through `pgoutput` to
the Compose Kafka broker over TLS.

From `on-premises/docker`, with the usual `.env` configured:

```bash
docker compose --profile cdc up -d debezium-register
docker compose logs debezium-postgres-init debezium-register
curl --fail http://localhost:8083/connectors/compose-postgres/status
```

The command starts the required services and applies the connector configuration.
Both the connector and its task should report `RUNNING`. The worker health check
only checks REST availability; `debezium-register` additionally checks task status.
The REST port is bound to localhost and configurable with `DEBEZIUM_PORT`.

PostgreSQL's `wal_level=logical`, replication slots, and WAL senders are configured
as server arguments, so existing data volumes work after the service is recreated.
Applying this configuration for the first time briefly restarts PostgreSQL.

## Capture scope and authentication

- `POSTGRES_DB` selects one existing database. Each additional database requires
  its own connector, publication, and unique replication slot.
- `DEBEZIUM_SCHEMA` selects one existing lowercase schema, default `public`.
  The publication includes future tables in that schema automatically.
- `DEBEZIUM_TOPIC_PREFIX` defaults to `postgres`. Table topics are named
  `<prefix>.<schema>.<table>`, for example `postgres.public.customers`.
- Records retain the Debezium JSON envelope (`before`, `after`, `source`, `op`).
  Operations are `r` for snapshot reads, `c` for inserts, `u` for updates, and
  `d` for deletes. Deletes also produce a Kafka tombstone.

The idempotent PostgreSQL initializer creates the `debezium` login with
`REPLICATION` and `pg_read_all_data`. It has read access to existing and future
tables, but no write privileges, superuser privileges, or row security bypass.
The publication `dbz_compose_publication` limits streaming to the selected schema;
the connector uses the same schema filter. Tables with row security may need
explicit policies for snapshots.

The initializer authenticates with the existing administrator certificate or
password according to `POSTGRES_MTLS_ENABLED`. It generates a separate Debezium
client certificate and persistent random password. The worker receives only its
own PostgreSQL credentials in the `debezium-postgres-config` volume. PostgreSQL
uses `verify-full`; Kafka uses the existing PKCS12 truststore and hostname
verification. Kafka Connect resolves the database password through a file config
provider, keeping it out of the connector JSON and Kafka configuration topic.

Give captured tables a primary key for reliable update/delete keys. Tables without
a primary key need an appropriate replica identity before updates/deletes; use
`ALTER TABLE ... REPLICA IDENTITY FULL` when full previous row values are required.

## Verify a change

With the default database and schema, create an example table and changes:

```bash
docker compose exec -T postgres sh -c \
  'psql -X -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1' <<'SQL'
CREATE TABLE public.cdc_example (id integer PRIMARY KEY, value text);
INSERT INTO public.cdc_example VALUES (1, 'created');
UPDATE public.cdc_example SET value = 'updated' WHERE id = 1;
DELETE FROM public.cdc_example WHERE id = 1;
SQL

docker compose exec kafka-4 /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka-4:29092 \
  --consumer.config /etc/kafka/secrets/client.properties \
  --topic postgres.public.cdc_example --from-beginning --max-messages 4
```

Expect `c`, `u`, `d`, and `null`. With multiple partitions, ordering is guaranteed
per key. Existing rows are snapshotted only on the first start; tables introduced
later stream new changes, and adding pre-populated tables requires a separate
snapshot if their historical rows are needed.

## Restarts and changes

Kafka retains connector configuration, offsets, and status in `_debezium_configs`,
`_debezium_offsets`, and `_debezium_status`. Their replication factor is one for
this single-broker development stack. PostgreSQL retains the replication slot
`dbz_compose_postgres` on shutdown. Keep both PostgreSQL and Kafka data volumes
to resume streaming; consumers should tolerate duplicate events after recovery.

After editing the connector JSON, rerun registration:

```bash
docker compose --profile cdc run --rm --no-deps debezium-register
```

After changing `.env` settings or regenerating TLS certificates, rerun the
initializer, recreate the worker to load the settings, and register again:

```bash
docker compose --profile cdc run --rm --no-deps debezium-postgres-init
docker compose --profile cdc up -d --no-deps --force-recreate debezium
docker compose --profile cdc run --rm --no-deps debezium-register
```

Keep database, slot, and topic prefix stable once offsets exist. Changing them
requires planning a new connector/snapshot rather than reusing unrelated offsets.
Changing capture scope does not automatically snapshot historical rows.

Stopping Debezium retains WAL for recovery. Monitor slot lag if it remains stopped:

```sql
SELECT slot_name, active,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained_wal
FROM pg_replication_slots
WHERE slot_name = 'dbz_compose_postgres';
```

For permanent removal, delete the connector through the REST API, stop the worker,
then deliberately drop its inactive replication slot and publication. Dropping a slot discards the
ability to resume from that retained WAL; do not do this for ordinary restarts.

Reference: [Debezium PostgreSQL connector documentation](https://debezium.io/documentation/reference/3.3/connectors/postgresql.html).
