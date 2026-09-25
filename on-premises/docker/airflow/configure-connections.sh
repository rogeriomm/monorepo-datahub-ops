#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

postgres_tls_dir=/etc/postgresql/tls
postgres_runtime_tls_dir=${AIRFLOW_HOME:-/opt/airflow}/tls/postgresql
seaweedfs_tls_dir=/etc/seaweedfs/tls
trino_tls_dir=/etc/trino/tls

required_files=(
  "${postgres_tls_dir}/ca.crt"
  "${postgres_tls_dir}/client.crt"
  "${postgres_tls_dir}/client.key"
  "${seaweedfs_tls_dir}/ca.crt"
  "${trino_tls_dir}/ca.crt"
  "${trino_tls_dir}/trino-client.crt"
  "${trino_tls_dir}/trino-client-key"
)

for required_file in "${required_files[@]}"; do
  if [[ ! -r "${required_file}" ]]; then
    echo "Airflow connection certificate is missing or unreadable: ${required_file}" >&2
    exit 1
  fi
done

install -d -m 0700 "${postgres_runtime_tls_dir}"
install -m 0600 \
  "${postgres_tls_dir}/client.key" \
  "${postgres_runtime_tls_dir}/client.key"

airflow db migrate

replace_connection() {
  local connection_id=$1
  shift

  airflow connections delete "${connection_id}" >/dev/null 2>&1 || true
  airflow connections add "${connection_id}" "$@"
}

replace_connection postgres_default \
  --conn-type postgres \
  --conn-host postgres \
  --conn-login "${POSTGRES_USER}" \
  --conn-password "${POSTGRES_PASSWORD}" \
  --conn-port 5432 \
  --conn-schema "${POSTGRES_DB}" \
  --conn-extra "{\"sslmode\":\"verify-full\",\"sslrootcert\":\"/etc/postgresql/tls/ca.crt\",\"sslcert\":\"/etc/postgresql/tls/client.crt\",\"sslkey\":\"${postgres_runtime_tls_dir}/client.key\"}"

replace_connection aws_default \
  --conn-type aws \
  --conn-login "${SEAWEEDFS_ACCESS_KEY_ID}" \
  --conn-password "${SEAWEEDFS_SECRET_ACCESS_KEY}" \
  --conn-extra "{\"endpoint_url\":\"https://seaweedfs:8333\",\"region_name\":\"${SEAWEEDFS_REGION}\",\"verify\":\"${seaweedfs_tls_dir}/ca.crt\",\"config_kwargs\":{\"s3\":{\"addressing_style\":\"path\"}}}"

replace_connection trino_default \
  --conn-type trino \
  --conn-host trino \
  --conn-login "${TRINO_CLIENT_NAME}" \
  --conn-port 8443 \
  --conn-schema runtime \
  --conn-extra '{"protocol":"https","catalog":"system","verify":"/etc/trino/tls/ca.crt","auth":"certs","certs__client_cert_path":"/etc/trino/tls/trino-client.crt","certs__client_key_path":"/etc/trino/tls/trino-client-key"}'

rm -f /opt/airflow/airflow-webserver.pid
exec "$@"
