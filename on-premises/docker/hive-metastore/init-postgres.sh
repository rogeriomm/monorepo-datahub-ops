#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail
umask 077

certificate_dir=/etc/postgresql/tls
config_dir=/etc/hive/postgres
temporary_dir=$(mktemp -d)
trap 'rm -rf "${temporary_dir}"' EXIT

export PGHOST=postgres PGPORT=5432 PGCONNECT_TIMEOUT=10
export PGUSER=${POSTGRES_USER:?POSTGRES_USER must be set}
export PGDATABASE=${POSTGRES_DB:?POSTGRES_DB must be set}
export PGSSLMODE=verify-full PGSSLROOTCERT=${certificate_dir}/ca.crt
if [[ "${POSTGRES_MTLS_ENABLED:-true}" == true ]]; then
  # libpq requires the key to be owned by the connecting OS user.
  install -m 600 "${certificate_dir}/client.key" "${temporary_dir}/admin.key"
  export PGSSLCERT=${certificate_dir}/client.crt
  export PGSSLKEY=${temporary_dir}/admin.key
else
  export PGPASSWORD=${POSTGRES_PASSWORD:?POSTGRES_PASSWORD must be set}
fi

install -d -m 755 "${config_dir}" "${config_dir}/conf"
# Keep the generated password stable across restarts, including TLS mode changes.
if [[ ! -s "${config_dir}/password" ]]; then
  openssl rand -hex 32 > "${config_dir}/password"
fi
export HIVE_DATABASE_PASSWORD=$(<"${config_dir}/password")
if [[ ! "${HIVE_DATABASE_PASSWORD}" =~ ^[a-f0-9]{64}$ ]]; then
  echo 'Invalid generated Hive database password' >&2
  exit 1
fi

# This runs for both fresh and existing PostgreSQL volumes. Refuse to reuse an
# administrative role or a database owned by another application.
psql --no-psqlrc --no-password --set=ON_ERROR_STOP=1 <<'SQL'
DO $$
BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'hive'
             AND (rolsuper OR rolcreatedb OR rolcreaterole OR rolreplication OR rolbypassrls)) THEN
    RAISE EXCEPTION 'The existing hive role has administrative privileges';
  END IF;
  IF EXISTS (SELECT FROM pg_database WHERE datname = 'hive_metastore'
             AND pg_get_userbyid(datdba) <> 'hive') THEN
    RAISE EXCEPTION 'The existing hive_metastore database is not owned by hive';
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'hive') THEN
    CREATE ROLE hive LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
  END IF;
END $$;
\getenv hive_password HIVE_DATABASE_PASSWORD
ALTER ROLE hive LOGIN PASSWORD :'hive_password';
SELECT 'CREATE DATABASE hive_metastore OWNER hive'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hive_metastore')
\gexec
REVOKE ALL ON DATABASE hive_metastore FROM PUBLIC;
SQL

# A dedicated certificate preserves PostgreSQL's certificate authentication;
# Hive never receives the PostgreSQL administrator's key or the CA private key.
openssl req -new -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=hive' -addext 'extendedKeyUsage=clientAuth' \
  -keyout "${temporary_dir}/hive.key" -out "${temporary_dir}/hive.csr" 2>/dev/null
openssl x509 -req -sha256 -days 825 -copy_extensions copy \
  -in "${temporary_dir}/hive.csr" \
  -CA "${certificate_dir}/ca.crt" -CAkey "${certificate_dir}/ca.key" \
  -set_serial "0x$(openssl rand -hex 16)" \
  -out "${temporary_dir}/hive.crt"
openssl pkcs12 -export -name user \
  -inkey "${temporary_dir}/hive.key" -in "${temporary_dir}/hive.crt" \
  -certfile "${certificate_dir}/ca.crt" \
  -passout pass: -out "${temporary_dir}/hive.p12"
install -m 644 "${certificate_dir}/ca.crt" "${config_dir}/ca.crt"
install -m 600 -o 1000 -g 1000 "${temporary_dir}/hive.p12" "${config_dir}/hive.p12"

# metastore-site.xml is loaded by both schematool and the metastore. Unlike
# hive-site.xml, the upstream entrypoint does not overwrite it on restart.
cat > "${temporary_dir}/metastore-site.xml" <<XML
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>org.postgresql.Driver</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:postgresql://postgres:5432/hive_metastore?sslmode=verify-full&amp;sslrootcert=${config_dir}/ca.crt&amp;sslkey=${config_dir}/hive.p12&amp;sslpassword=</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hive</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>${HIVE_DATABASE_PASSWORD}</value>
  </property>
  <property>
    <name>hive.metastore.schema.verification</name>
    <value>true</value>
  </property>
</configuration>
XML
install -m 600 -o 1000 -g 1000 \
  "${temporary_dir}/metastore-site.xml" "${config_dir}/conf/metastore-site.xml"
echo 'PostgreSQL database hive_metastore and dedicated hive credentials are ready.'
