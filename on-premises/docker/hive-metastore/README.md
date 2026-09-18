# Hive Metastore

The `trino` Compose profile uses the shared `postgres` service for Hive metadata.
The `hive-postgres-init` service creates the `hive_metastore` database owned by
the dedicated `hive` login, which has no administrative privileges. Initialization
also works with an existing PostgreSQL volume and can be rerun safely.

Hive connects over TLS with server certificate verification. Its own client
certificate supports `POSTGRES_MTLS_ENABLED=true`; a generated password supports
password authentication when that setting is `false`. Credentials and the custom
Hive configuration live in the `hive-postgres-config` Docker volume. No manual
Hive password setting is needed. The initializer uses the existing PostgreSQL
administrator credentials and CA to provision this identity; Hive receives only
its own credentials and the public CA certificate.

From `on-premises/docker`, after configuring `.env`:

```sh
docker compose --profile trino up -d --build hive-metastore hive-server2 trino
```

The `hive-metastore-catalog-init` service creates isolated Hive Metastore
catalogs for Trino. The `iceberg` catalog uses `s3a://trino-lakehouse`, and the
`delta` catalog uses `s3a://delta-lakehouse`.

The metastore service uses `iceberg` as its default catalog because Trino's
filtered table-name Thrift call does not carry a catalog name. Other Trino
metastore calls continue to use the catalog configured by
`hive.metastore.thrift.catalog-name`.

The Hive image includes the PostgreSQL JDBC driver. Hive initializes or upgrades
its PostgreSQL schema before starting the metastore. Metadata persists in
`postgres-data`; the existing `hive-metastore-data` warehouse volume is retained.

## BeeLine

BeeLine is a JDBC client for HiveServer2; it cannot connect directly to the Hive
Metastore Thrift port. Start `hive-server2`, then open an interactive session:

```sh
docker compose exec hive-server2 \
  beeline -u 'jdbc:hive2://localhost:10000/default' -n hive
```

The same client can be run from the Metastore container:

```sh
docker compose exec hive-metastore \
  beeline -u 'jdbc:hive2://hive-server2:10000/default' -n hive
```

At the `beeline>` prompt, list databases and tables with:

```sql
SHOW DATABASES;
SHOW TABLES IN default;
SHOW TABLES IN database_name;
```

Hive uses the `hive` Metastore catalog by default. To inspect a catalog created
for Trino, set it before the first metadata query in the BeeLine session:

```sql
SET metastore.catalog.default=iceberg;
SHOW DATABASES;
SHOW TABLES IN database_name;
```

Use `delta` instead of `iceberg` for the Delta Lake catalog.

For a one-shot listing from the `iceberg` catalog, run:

```sh
docker compose exec hive-server2 \
  beeline --silent=true --outputformat=table \
  -u 'jdbc:hive2://localhost:10000/default' -n hive \
  -e 'SET metastore.catalog.default=iceberg; SHOW TABLES IN database_name;'
```

Do not pass `-T` to `docker compose exec` for these commands. BeeLine in the Hive
4.2.1 image requires the pseudo-terminal that Compose allocates by default.

Switching database backends does **not** migrate existing Derby metadata. Back up
the old metastore before recreating its container, and migrate or re-register
existing tables if they must be retained. Lakehouse objects in SeaweedFS remain
in place.

After rotating the PostgreSQL CA, rerun the initializer and recreate Hive:

```sh
docker compose --profile trino run --rm hive-postgres-init
docker compose --profile trino up -d --force-recreate hive-metastore
```
