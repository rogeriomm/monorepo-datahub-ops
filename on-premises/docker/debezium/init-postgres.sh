#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
umask 077

certificate_dir=/etc/postgresql/tls
config_dir=/etc/debezium/postgres
temporary_dir=$(mktemp -d)
trap 'rm -rf "${temporary_dir}"' EXIT

export PGHOST=postgres PGPORT=5432 PGCONNECT_TIMEOUT=10
export PGUSER=${POSTGRES_USER:?POSTGRES_USER must be set}
export PGDATABASE=${POSTGRES_DB:?POSTGRES_DB must be set}
export PGSSLMODE=verify-full PGSSLROOTCERT=${certificate_dir}/ca.crt
if [[ "${POSTGRES_MTLS_ENABLED:-true}" == true ]]; then
  install -m 600 "${certificate_dir}/client.key" "${temporary_dir}/admin.key"
  export PGSSLCERT=${certificate_dir}/client.crt PGSSLKEY=${temporary_dir}/admin.key
else
  export PGPASSWORD=${POSTGRES_PASSWORD:?POSTGRES_PASSWORD must be set}
fi

export DEBEZIUM_SCHEMA=${DEBEZIUM_SCHEMA:-public}
export DEBEZIUM_PUBLICATION_NAME=${DEBEZIUM_PUBLICATION_NAME:-dbz_compose_publication}
# One schema name, also used as a quoted literal in the connector's Java regex.
if [[ ! "${DEBEZIUM_SCHEMA}" =~ ^[a-z_][a-z0-9_]{0,62}$ ]]; then
  echo 'DEBEZIUM_SCHEMA must be a lowercase PostgreSQL schema name' >&2
  exit 1
fi
if [[ ! "${DEBEZIUM_PUBLICATION_NAME}" =~ ^[a-z_][a-z0-9_]{0,62}$ ]]; then
  echo 'DEBEZIUM_PUBLICATION_NAME must be a lowercase PostgreSQL identifier' >&2
  exit 1
fi

install -d -m 755 "${config_dir}"
if [[ ! -s "${config_dir}/password" ]]; then
  openssl rand -hex 32 > "${config_dir}/password"
fi
export DEBEZIUM_DATABASE_PASSWORD=$(<"${config_dir}/password")
if [[ ! "${DEBEZIUM_DATABASE_PASSWORD}" =~ ^[a-f0-9]{64}$ ]]; then
  echo 'Invalid generated Debezium database password' >&2
  exit 1
fi

# Runs against existing volumes too; no docker-entrypoint-initdb.d dependency.
psql --no-psqlrc --no-password --set=ON_ERROR_STOP=1 <<'SQL'
\getenv cdc_password DEBEZIUM_DATABASE_PASSWORD
\getenv cdc_schema DEBEZIUM_SCHEMA
\getenv cdc_database PGDATABASE
\getenv cdc_publication DEBEZIUM_PUBLICATION_NAME
BEGIN;
DO $$
BEGIN
  IF current_setting('wal_level') <> 'logical' THEN
    RAISE EXCEPTION 'Restart the Compose postgres service to enable wal_level=logical';
  END IF;
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'debezium'
             AND (rolsuper OR rolcreatedb OR rolcreaterole OR rolbypassrls)) THEN
    RAISE EXCEPTION 'The existing debezium role has administrative privileges';
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'debezium') THEN
    CREATE ROLE debezium LOGIN REPLICATION NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
  END IF;
END $$;
ALTER ROLE debezium LOGIN REPLICATION PASSWORD :'cdc_password';
GRANT CONNECT ON DATABASE :"cdc_database" TO debezium;
-- Includes future tables regardless of their owner, without granting writes or RLS bypass.
GRANT pg_read_all_data TO debezium;
SELECT format(
  'CREATE PUBLICATION %I FOR TABLES IN SCHEMA %I',
  :'cdc_publication', :'cdc_schema'
)
WHERE NOT EXISTS (
  SELECT FROM pg_publication WHERE pubname = :'cdc_publication'
)
\gexec
SELECT format(
  'ALTER PUBLICATION %I SET TABLES IN SCHEMA %I',
  :'cdc_publication', :'cdc_schema'
)
\gexec
COMMIT;
SQL

# Only the dedicated client identity is exported to the Connect worker.
openssl req -new -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=debezium' -addext 'extendedKeyUsage=clientAuth' \
  -keyout "${temporary_dir}/debezium.key" -out "${temporary_dir}/debezium.csr" 2>/dev/null
openssl x509 -req -sha256 -days 825 -copy_extensions copy \
  -in "${temporary_dir}/debezium.csr" \
  -CA "${certificate_dir}/ca.crt" -CAkey "${certificate_dir}/ca.key" \
  -set_serial "0x$(openssl rand -hex 16)" \
  -out "${temporary_dir}/debezium.crt"
openssl pkcs12 -export -name user \
  -inkey "${temporary_dir}/debezium.key" -in "${temporary_dir}/debezium.crt" \
  -certfile "${certificate_dir}/ca.crt" \
  -passout pass: -out "${temporary_dir}/debezium.p12"
printf 'password=%s\n' "${DEBEZIUM_DATABASE_PASSWORD}" > "${temporary_dir}/credentials.properties"
install -m 644 "${certificate_dir}/ca.crt" "${config_dir}/ca.crt"
# The upstream Debezium image runs as kafka (UID 1001).
install -m 600 -o 1001 -g 1001 \
  "${temporary_dir}/debezium.p12" "${temporary_dir}/credentials.properties" "${config_dir}/"
echo 'PostgreSQL Debezium replication account, publication, and TLS credentials are ready.'
