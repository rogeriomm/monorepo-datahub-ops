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
docker compose --profile trino up -d --build hive-metastore trino
```

The Hive image includes the PostgreSQL JDBC driver. Hive initializes or upgrades
its PostgreSQL schema before starting the metastore. Metadata persists in
`postgres-data`; the existing `hive-metastore-data` warehouse volume is retained.

Switching database backends does **not** migrate existing Derby metadata. Back up
the old metastore before recreating its container, and migrate or re-register
existing tables if they must be retained. Lakehouse objects in SeaweedFS remain
in place.

After rotating the PostgreSQL CA, rerun the initializer and recreate Hive:

```sh
docker compose --profile trino run --rm hive-postgres-init
docker compose --profile trino up -d --force-recreate hive-metastore
```
