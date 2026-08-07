#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

tls_dir=/etc/trino/tls
store_password=${TRINO_TLS_STORE_PASSWORD:-changeit}
client_name=${TRINO_CLIENT_NAME:-trino-client}
client_store_password=${TRINO_CLIENT_STORE_PASSWORD:-changeit}
external_hostname=${TRINO_HOSTNAME:?TRINO_HOSTNAME must be set}
ca_keystore=${tls_dir}/trino-ca.p12
server_keystore=${tls_dir}/trino.keystore.p12
server_truststore=${tls_dir}/trino.truststore.p12
client_keystore=${tls_dir}/trino-client.p12

if (( ${#store_password} < 6 )); then
  echo "TRINO_TLS_STORE_PASSWORD must contain at least 6 characters" >&2
  exit 1
fi

if (( ${#client_store_password} < 6 )); then
  echo "TRINO_CLIENT_STORE_PASSWORD must contain at least 6 characters" >&2
  exit 1
fi

if [[ ! "${client_name}" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$ ]]; then
  echo "Invalid TRINO_CLIENT_NAME: ${client_name}" >&2
  exit 1
fi

if (( ${#external_hostname} > 253 )) \
  || [[ ! "${external_hostname}" =~ ^[A-Za-z0-9.-]+$ ]] \
  || [[ "${external_hostname}" == .* ]] \
  || [[ "${external_hostname}" == *. ]] \
  || [[ "${external_hostname}" == *..* ]]; then
  echo "Invalid TRINO_HOSTNAME: ${external_hostname}" >&2
  exit 1
fi

IFS=. read -r -a hostname_labels <<< "${external_hostname}"
for hostname_label in "${hostname_labels[@]}"; do
  if (( ${#hostname_label} > 63 )) \
    || [[ "${hostname_label}" == -* ]] \
    || [[ "${hostname_label}" == *- ]]; then
    echo "Invalid TRINO_HOSTNAME: ${external_hostname}" >&2
    exit 1
  fi
done

mkdir -p "${tls_dir}"
umask 077

if [[ ! -s "${tls_dir}/internal-shared-secret" ]]; then
  dd if=/dev/urandom bs=64 count=1 status=none \
    | base64 \
    | tr -d '\n' > "${tls_dir}/internal-shared-secret"
fi
export TRINO_INTERNAL_SHARED_SECRET="$(<"${tls_dir}/internal-shared-secret")"

regenerate_server=false
for required_file in ca.crt trino.crt "$(basename "${ca_keystore}")" "$(basename "${server_keystore}")"; do
  if [[ ! -s "${tls_dir}/${required_file}" ]]; then
    regenerate_server=true
  fi
done

if [[ ! -s "${tls_dir}/keystore-password" ]] \
  || [[ "$(<"${tls_dir}/keystore-password")" != "${store_password}" ]]; then
  regenerate_server=true
fi

if [[ ! -s "${tls_dir}/certificate-hostname" ]] \
  || [[ "$(<"${tls_dir}/certificate-hostname")" != "${external_hostname}" ]]; then
  regenerate_server=true
fi

if [[ "${regenerate_server}" == true ]]; then
  echo "===> Generating the Trino server certificate and PKCS12 keystore ..."
  rm -f \
    "${tls_dir}/ca.crt" \
    "${tls_dir}/trino.crt" \
    "${tls_dir}/trino.csr" \
    "${ca_keystore}" \
    "${server_keystore}"

  keytool \
    -genkeypair \
    -alias trino-ca \
    -keyalg RSA \
    -keysize 3072 \
    -sigalg SHA256withRSA \
    -dname "CN=local-trino-ca" \
    -validity 3650 \
    -ext BC=ca:true \
    -ext KU=keyCertSign,cRLSign \
    -storetype PKCS12 \
    -keystore "${ca_keystore}" \
    -storepass "${store_password}" \
    -keypass "${store_password}"

  keytool \
    -exportcert \
    -rfc \
    -alias trino-ca \
    -keystore "${ca_keystore}" \
    -storepass "${store_password}" \
    -file "${tls_dir}/ca.crt"

  keytool \
    -genkeypair \
    -alias trino \
    -keyalg RSA \
    -keysize 2048 \
    -sigalg SHA256withRSA \
    -dname "CN=${external_hostname}" \
    -validity 825 \
    -ext "SAN=DNS:${external_hostname},DNS:trino,DNS:localhost,IP:127.0.0.1" \
    -ext KU=digitalSignature,keyEncipherment \
    -ext EKU=serverAuth \
    -storetype PKCS12 \
    -keystore "${server_keystore}" \
    -storepass "${store_password}" \
    -keypass "${store_password}"

  keytool \
    -certreq \
    -alias trino \
    -keystore "${server_keystore}" \
    -storepass "${store_password}" \
    -file "${tls_dir}/trino.csr" \
    -ext "SAN=DNS:${external_hostname},DNS:trino,DNS:localhost,IP:127.0.0.1" \
    -ext KU=digitalSignature,keyEncipherment \
    -ext EKU=serverAuth

  keytool \
    -gencert \
    -rfc \
    -alias trino-ca \
    -keystore "${ca_keystore}" \
    -storepass "${store_password}" \
    -infile "${tls_dir}/trino.csr" \
    -outfile "${tls_dir}/trino.crt" \
    -validity 825 \
    -ext "SAN=DNS:${external_hostname},DNS:trino,DNS:localhost,IP:127.0.0.1" \
    -ext KU=digitalSignature,keyEncipherment \
    -ext EKU=serverAuth

  keytool \
    -importcert \
    -noprompt \
    -alias trino-ca \
    -file "${tls_dir}/ca.crt" \
    -keystore "${server_keystore}" \
    -storepass "${store_password}"

  keytool \
    -importcert \
    -alias trino \
    -file "${tls_dir}/trino.crt" \
    -keystore "${server_keystore}" \
    -storepass "${store_password}"

  rm -f "${tls_dir}/trino.csr"
fi

regenerate_client=${regenerate_server}
for required_file in trino-client.crt "$(basename "${client_keystore}")" "$(basename "${server_truststore}")"; do
  if [[ ! -s "${tls_dir}/${required_file}" ]]; then
    regenerate_client=true
  fi
done

if [[ ! -s "${tls_dir}/client-password" ]] \
  || [[ "$(<"${tls_dir}/client-password")" != "${client_store_password}" ]]; then
  regenerate_client=true
fi

if [[ ! -s "${tls_dir}/client-name" ]] \
  || [[ "$(<"${tls_dir}/client-name")" != "${client_name}" ]]; then
  regenerate_client=true
fi

if [[ "${regenerate_client}" == true ]]; then
  echo "===> Generating the reusable Trino client certificate and truststore ..."
  rm -f \
    "${tls_dir}/trino-client.crt" \
    "${tls_dir}/trino-client.csr" \
    "${client_keystore}" \
    "${server_truststore}"

  keytool \
    -importcert \
    -noprompt \
    -alias trino-ca \
    -file "${tls_dir}/ca.crt" \
    -storetype PKCS12 \
    -keystore "${server_truststore}" \
    -storepass "${store_password}"

  keytool \
    -genkeypair \
    -alias "${client_name}" \
    -keyalg RSA \
    -keysize 2048 \
    -sigalg SHA256withRSA \
    -dname "CN=${client_name}" \
    -validity 825 \
    -ext KU=digitalSignature,keyEncipherment \
    -ext EKU=clientAuth \
    -storetype PKCS12 \
    -keystore "${client_keystore}" \
    -storepass "${client_store_password}" \
    -keypass "${client_store_password}"

  keytool \
    -certreq \
    -alias "${client_name}" \
    -keystore "${client_keystore}" \
    -storepass "${client_store_password}" \
    -file "${tls_dir}/trino-client.csr" \
    -ext KU=digitalSignature,keyEncipherment \
    -ext EKU=clientAuth

  keytool \
    -gencert \
    -rfc \
    -alias trino-ca \
    -keystore "${ca_keystore}" \
    -storepass "${store_password}" \
    -infile "${tls_dir}/trino-client.csr" \
    -outfile "${tls_dir}/trino-client.crt" \
    -validity 825 \
    -ext KU=digitalSignature,keyEncipherment \
    -ext EKU=clientAuth

  keytool \
    -importcert \
    -noprompt \
    -alias trino-ca \
    -file "${tls_dir}/ca.crt" \
    -keystore "${client_keystore}" \
    -storepass "${client_store_password}"

  keytool \
    -importcert \
    -alias "${client_name}" \
    -file "${tls_dir}/trino-client.crt" \
    -keystore "${client_keystore}" \
    -storepass "${client_store_password}"

  rm -f "${tls_dir}/trino-client.csr"
fi

printf '%s' "${store_password}" > "${tls_dir}/keystore-password"
printf '%s' "${external_hostname}" > "${tls_dir}/certificate-hostname"
printf '%s' "${client_store_password}" > "${tls_dir}/client-password"
printf '%s' "${client_name}" > "${tls_dir}/client-name"

chmod 600 \
  "${ca_keystore}" \
  "${server_keystore}" \
  "${server_truststore}" \
  "${client_keystore}" \
  "${tls_dir}/keystore-password" \
  "${tls_dir}/client-password" \
  "${tls_dir}/client-name" \
  "${tls_dir}/certificate-hostname" \
  "${tls_dir}/internal-shared-secret"
chmod 644 \
  "${tls_dir}/ca.crt" \
  "${tls_dir}/trino.crt" \
  "${tls_dir}/trino-client.crt"

exec "$@"
