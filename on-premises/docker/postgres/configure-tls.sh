#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

certificate_dir=/etc/postgresql/tls
legacy_tls_dir=/var/lib/postgresql/tls
tls_dir=/var/run/postgresql/tls
external_hostname=${POSTGRES_HOSTNAME:-localhost}
client_name=${POSTGRES_USER:?POSTGRES_USER must be set}
client_store_password=${POSTGRES_CLIENT_STORE_PASSWORD:-changeit}
mtls_enabled=${POSTGRES_MTLS_ENABLED:-true}
client_keystore=${tls_dir}/postgres-client.p12

pgdata=${PGDATA:?PGDATA must be set}
# PostgreSQL 18 uses a versioned parent directory that must remain traversable
# after the official entrypoint drops from root to the postgres user.
install -d -m 700 -o postgres -g postgres \
  "$(dirname "${pgdata}")" \
  "${pgdata}"

if (( ${#client_store_password} < 6 )); then
  echo "POSTGRES_CLIENT_STORE_PASSWORD must contain at least 6 characters" >&2
  exit 1
fi

if [[ "${mtls_enabled}" != true && "${mtls_enabled}" != false ]]; then
  echo "POSTGRES_MTLS_ENABLED must be either true or false" >&2
  exit 1
fi

if [[ ! "${client_name}" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,62}$ ]]; then
  echo "POSTGRES_USER cannot be used as a certificate common name: ${client_name}" >&2
  exit 1
fi

if (( ${#external_hostname} > 253 )) \
  || [[ ! "${external_hostname}" =~ ^[A-Za-z0-9.-]+$ ]] \
  || [[ "${external_hostname}" == .* ]] \
  || [[ "${external_hostname}" == *. ]] \
  || [[ "${external_hostname}" == *..* ]]; then
  echo "Invalid POSTGRES_HOSTNAME: ${external_hostname}" >&2
  exit 1
fi

IFS=. read -r -a hostname_labels <<< "${external_hostname}"
for hostname_label in "${hostname_labels[@]}"; do
  if (( ${#hostname_label} > 63 )) \
    || [[ "${hostname_label}" == -* ]] \
    || [[ "${hostname_label}" == *- ]]; then
    echo "Invalid POSTGRES_HOSTNAME: ${external_hostname}" >&2
    exit 1
  fi
done

install -d "${certificate_dir}"
install -d -m 700 -o postgres -g postgres "${tls_dir}"
umask 077

persistent_tls_files=(
  ca.crt
  ca.key
  server.crt
  server.key
  client.crt
  client.key
  postgres-client.p12
  certificate-hostname
  client-name
  client-password
)

# The bind-mounted certificate directory is authoritative, like Trino's
# /etc/trino/tls directory. Fall back to the old Docker-volume location once
# so existing installations retain their CA during this layout migration.
certificate_source_dir=${certificate_dir}
for required_file in "${persistent_tls_files[@]}"; do
  if [[ ! -s "${certificate_source_dir}/${required_file}" ]]; then
    certificate_source_dir=${legacy_tls_dir}
    break
  fi
done

for required_file in "${persistent_tls_files[@]}"; do
  if [[ ! -s "${certificate_source_dir}/${required_file}" ]]; then
    certificate_source_dir=
    break
  fi
done

rm -f \
  "${tls_dir}/ca.crt" \
  "${tls_dir}/ca.key" \
  "${tls_dir}/ca.srl" \
  "${tls_dir}/server.crt" \
  "${tls_dir}/server.csr" \
  "${tls_dir}/server.key" \
  "${tls_dir}/client.crt" \
  "${tls_dir}/client.csr" \
  "${tls_dir}/client.key" \
  "${client_keystore}" \
  "${tls_dir}/certificate-hostname" \
  "${tls_dir}/client-name" \
  "${tls_dir}/client-password" \
  "${tls_dir}/postgres-password" \
  "${tls_dir}/pg_hba.conf"

if [[ -n "${certificate_source_dir}" ]]; then
  for required_file in "${persistent_tls_files[@]}"; do
    install -m 600 \
      "${certificate_source_dir}/${required_file}" \
      "${tls_dir}/${required_file}"
  done
fi

regenerate_server=false
for required_file in ca.crt ca.key server.crt server.key; do
  if [[ ! -s "${tls_dir}/${required_file}" ]]; then
    regenerate_server=true
  fi
done

if [[ ! -s "${tls_dir}/certificate-hostname" ]] \
  || [[ "$(<"${tls_dir}/certificate-hostname")" != "${external_hostname}" ]]; then
  regenerate_server=true
fi

if [[ "${regenerate_server}" == true ]]; then
  echo "===> Generating the PostgreSQL CA and server certificate ..."
  rm -f \
    "${tls_dir}/ca.crt" \
    "${tls_dir}/ca.key" \
    "${tls_dir}/server.crt" \
    "${tls_dir}/server.csr" \
    "${tls_dir}/server.key"

  openssl req \
    -x509 \
    -newkey rsa:3072 \
    -nodes \
    -sha256 \
    -days 3650 \
    -subj "/CN=local-postgres-ca" \
    -addext "basicConstraints=critical,CA:TRUE" \
    -addext "keyUsage=critical,keyCertSign,cRLSign" \
    -keyout "${tls_dir}/ca.key" \
    -out "${tls_dir}/ca.crt"

  openssl req \
    -new \
    -newkey rsa:2048 \
    -nodes \
    -sha256 \
    -subj "/CN=${external_hostname}" \
    -addext "subjectAltName=DNS:${external_hostname},DNS:postgres,DNS:localhost,IP:127.0.0.1" \
    -addext "keyUsage=critical,digitalSignature,keyEncipherment" \
    -addext "extendedKeyUsage=serverAuth" \
    -keyout "${tls_dir}/server.key" \
    -out "${tls_dir}/server.csr"

  openssl x509 \
    -req \
    -sha256 \
    -days 825 \
    -copy_extensions copy \
    -in "${tls_dir}/server.csr" \
    -CA "${tls_dir}/ca.crt" \
    -CAkey "${tls_dir}/ca.key" \
    -CAcreateserial \
    -out "${tls_dir}/server.crt"

  rm -f "${tls_dir}/server.csr" "${tls_dir}/ca.srl"
fi

regenerate_client=${regenerate_server}
for required_file in client.crt client.key; do
  if [[ ! -s "${tls_dir}/${required_file}" ]]; then
    regenerate_client=true
  fi
done

if [[ ! -s "${tls_dir}/client-name" ]] \
  || [[ "$(<"${tls_dir}/client-name")" != "${client_name}" ]]; then
  regenerate_client=true
fi

if [[ "${regenerate_client}" == true ]]; then
  echo "===> Generating the reusable PostgreSQL client certificate ..."
  rm -f \
    "${tls_dir}/client.crt" \
    "${tls_dir}/client.csr" \
    "${tls_dir}/client.key" \
    "${client_keystore}"

  openssl req \
    -new \
    -newkey rsa:2048 \
    -nodes \
    -sha256 \
    -subj "/CN=${client_name}" \
    -addext "keyUsage=critical,digitalSignature,keyEncipherment" \
    -addext "extendedKeyUsage=clientAuth" \
    -keyout "${tls_dir}/client.key" \
    -out "${tls_dir}/client.csr"

  openssl x509 \
    -req \
    -sha256 \
    -days 825 \
    -copy_extensions copy \
    -in "${tls_dir}/client.csr" \
    -CA "${tls_dir}/ca.crt" \
    -CAkey "${tls_dir}/ca.key" \
    -CAcreateserial \
    -out "${tls_dir}/client.crt"

  rm -f "${tls_dir}/client.csr" "${tls_dir}/ca.srl"
fi

regenerate_client_keystore=${regenerate_client}
if [[ ! -s "${client_keystore}" ]]; then
  regenerate_client_keystore=true
fi

if [[ ! -s "${tls_dir}/client-password" ]] \
  || [[ "$(<"${tls_dir}/client-password")" != "${client_store_password}" ]]; then
  regenerate_client_keystore=true
fi

if [[ "${regenerate_client_keystore}" == true ]]; then
  echo "===> Generating the reusable PostgreSQL client PKCS12 keystore ..."
  rm -f "${client_keystore}"
  openssl pkcs12 \
    -export \
    -name user \
    -inkey "${tls_dir}/client.key" \
    -in "${tls_dir}/client.crt" \
    -certfile "${tls_dir}/ca.crt" \
    -passout "pass:${client_store_password}" \
    -out "${client_keystore}"
fi

printf '%s' "${external_hostname}" > "${tls_dir}/certificate-hostname"
printf '%s' "${client_name}" > "${tls_dir}/client-name"
printf '%s' "${client_store_password}" > "${tls_dir}/client-password"

if [[ "${mtls_enabled}" == false ]]; then
  postgres_password=${POSTGRES_PASSWORD:?POSTGRES_PASSWORD must be set when mTLS is disabled}
  printf '%s' "${postgres_password}" > "${tls_dir}/postgres-password"
  unset postgres_password
fi

chown postgres:postgres "${tls_dir}"/*
chmod 600 \
  "${tls_dir}/ca.key" \
  "${tls_dir}/server.key" \
  "${tls_dir}/client.key" \
  "${client_keystore}" \
  "${tls_dir}/certificate-hostname" \
  "${tls_dir}/client-name" \
  "${tls_dir}/client-password"
if [[ "${mtls_enabled}" == false ]]; then
  chmod 600 "${tls_dir}/postgres-password"
fi
chmod 644 \
  "${tls_dir}/ca.crt" \
  "${tls_dir}/server.crt" \
  "${tls_dir}/client.crt"

export_uid=$(stat -c '%u' "${certificate_dir}")
export_gid=$(stat -c '%g' "${certificate_dir}")
install -m 644 -o "${export_uid}" -g "${export_gid}" \
  "${tls_dir}/ca.crt" \
  "${tls_dir}/server.crt" \
  "${tls_dir}/client.crt" \
  "${certificate_dir}/"
install -m 600 -o "${export_uid}" -g "${export_gid}" \
  "${tls_dir}/ca.key" \
  "${tls_dir}/server.key" \
  "${tls_dir}/client.key" \
  "${client_keystore}" \
  "${tls_dir}/certificate-hostname" \
  "${tls_dir}/client-name" \
  "${tls_dir}/client-password" \
  "${certificate_dir}/"

if [[ "${mtls_enabled}" == false ]]; then
  install -m 600 -o "${export_uid}" -g "${export_gid}" \
    "${tls_dir}/postgres-password" \
    "${certificate_dir}/postgres-password"
else
  rm -f "${certificate_dir}/postgres-password"
fi

if [[ "${mtls_enabled}" == true ]]; then
  host_authentication=cert
else
  host_authentication=scram-sha-256
fi

printf '%s\n' \
  'local all all trust' \
  "hostssl all all 0.0.0.0/0 ${host_authentication}" \
  "hostssl all all ::/0 ${host_authentication}" \
  'hostnossl all all 0.0.0.0/0 reject' \
  'hostnossl all all ::/0 reject' \
  > "${tls_dir}/pg_hba.conf"
chown postgres:postgres "${tls_dir}/pg_hba.conf"
chmod 600 "${tls_dir}/pg_hba.conf"

exec docker-entrypoint.sh "$@"
