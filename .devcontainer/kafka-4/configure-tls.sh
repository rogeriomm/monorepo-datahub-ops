#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

tls_dir=/etc/kafka/secrets
store_password=${KAFKA_TLS_STORE_PASSWORD:-changeit}
keystore=${tls_dir}/kafka.keystore.p12
truststore=${tls_dir}/kafka.truststore.p12

mkdir -p "${tls_dir}"

regenerate=false
for required_file in ca.crt ca.key kafka.crt kafka.key "$(basename "${keystore}")" "$(basename "${truststore}")"; do
  if [[ ! -s "${tls_dir}/${required_file}" ]]; then
    regenerate=true
  fi
done

if [[ ! -s "${tls_dir}/keystore-password" ]] || [[ "$(<"${tls_dir}/keystore-password")" != "${store_password}" ]]; then
  regenerate=true
fi

if [[ -s "${tls_dir}/kafka.crt" ]] && ! openssl x509 \
  -in "${tls_dir}/kafka.crt" \
  -noout \
  -checkhost kafka-4-backend >/dev/null 2>&1; then
  regenerate=true
fi

if [[ "${regenerate}" == true ]]; then
  echo "===> Generating the devcontainer Kafka TLS certificate and stores ..."
  rm -f \
    "${tls_dir}/ca.crt" \
    "${tls_dir}/ca.key" \
    "${tls_dir}/kafka.crt" \
    "${tls_dir}/kafka.csr" \
    "${tls_dir}/kafka.key" \
    "${tls_dir}/kafka-cert.ext" \
    "${keystore}" \
    "${truststore}"

  openssl genpkey \
    -algorithm RSA \
    -pkeyopt rsa_keygen_bits:2048 \
    -out "${tls_dir}/ca.key"
  openssl req \
    -x509 \
    -new \
    -sha256 \
    -days 3650 \
    -key "${tls_dir}/ca.key" \
    -subj "/CN=devcontainer-kafka-ca" \
    -addext "basicConstraints=critical,CA:TRUE" \
    -addext "keyUsage=critical,keyCertSign,cRLSign" \
    -out "${tls_dir}/ca.crt"

  openssl genpkey \
    -algorithm RSA \
    -pkeyopt rsa_keygen_bits:2048 \
    -out "${tls_dir}/kafka.key"
  openssl req \
    -new \
    -sha256 \
    -key "${tls_dir}/kafka.key" \
    -subj "/CN=kafka-4-backend" \
    -out "${tls_dir}/kafka.csr"

  cat > "${tls_dir}/kafka-cert.ext" <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectAltName=DNS:kafka-4-backend,DNS:kafka-4,DNS:localhost,IP:127.0.0.1
EOF

  openssl x509 \
    -req \
    -sha256 \
    -days 825 \
    -in "${tls_dir}/kafka.csr" \
    -CA "${tls_dir}/ca.crt" \
    -CAkey "${tls_dir}/ca.key" \
    -CAcreateserial \
    -extfile "${tls_dir}/kafka-cert.ext" \
    -out "${tls_dir}/kafka.crt"

  openssl pkcs12 \
    -export \
    -name kafka-4-backend \
    -in "${tls_dir}/kafka.crt" \
    -inkey "${tls_dir}/kafka.key" \
    -certfile "${tls_dir}/ca.crt" \
    -passout "pass:${store_password}" \
    -out "${keystore}"

  /opt/java/openjdk/bin/keytool \
    -importcert \
    -noprompt \
    -alias devcontainer-kafka-ca \
    -file "${tls_dir}/ca.crt" \
    -keystore "${truststore}" \
    -storetype PKCS12 \
    -storepass "${store_password}"

  rm -f \
    "${tls_dir}/ca.srl" \
    "${tls_dir}/kafka.csr" \
    "${tls_dir}/kafka-cert.ext"
fi

printf '%s' "${store_password}" > "${tls_dir}/keystore-password"
printf '%s' "${store_password}" > "${tls_dir}/key-password"
printf '%s' "${store_password}" > "${tls_dir}/truststore-password"
cat > "${tls_dir}/client.properties" <<EOF
security.protocol=SSL
ssl.truststore.location=${truststore}
ssl.truststore.password=${store_password}
ssl.truststore.type=PKCS12
ssl.endpoint.identification.algorithm=https
EOF

chmod 600 \
  "${tls_dir}/ca.key" \
  "${tls_dir}/kafka.key" \
  "${tls_dir}/keystore-password" \
  "${tls_dir}/key-password" \
  "${tls_dir}/truststore-password" \
  "${tls_dir}/client.properties"
chmod 644 \
  "${tls_dir}/ca.crt" \
  "${tls_dir}/kafka.crt" \
  "${keystore}" \
  "${truststore}"

exec /etc/kafka/docker/run "$@"
