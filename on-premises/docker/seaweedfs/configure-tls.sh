#!/bin/sh

set -eu

tls_dir=/etc/seaweedfs/tls
ca_certificate="${tls_dir}/ca.crt"
ca_key="${tls_dir}/ca.key"
server_certificate="${tls_dir}/server.crt"
server_key="${tls_dir}/server.key"

mkdir -p "${tls_dir}"

regenerate=false
for required_file in "${ca_certificate}" "${ca_key}" "${server_certificate}" "${server_key}"; do
  if [ ! -s "${required_file}" ]; then
    regenerate=true
  fi
done

if [ -s "${server_certificate}" ] && ! openssl x509 \
  -in "${server_certificate}" \
  -noout \
  -checkhost seaweedfs >/dev/null 2>&1; then
  regenerate=true
fi

if [ "${regenerate}" = true ]; then
  echo "Generating the devcontainer SeaweedFS TLS certificate ..."
  rm -f \
    "${ca_certificate}" \
    "${ca_key}" \
    "${tls_dir}/ca.srl" \
    "${server_certificate}" \
    "${tls_dir}/server.csr" \
    "${tls_dir}/server-cert.ext" \
    "${server_key}"

  openssl genpkey \
    -algorithm RSA \
    -pkeyopt rsa_keygen_bits:2048 \
    -out "${ca_key}"
  openssl req \
    -x509 \
    -new \
    -sha256 \
    -days 3650 \
    -key "${ca_key}" \
    -subj "/CN=devcontainer-seaweedfs-ca" \
    -addext "basicConstraints=critical,CA:TRUE" \
    -addext "keyUsage=critical,keyCertSign,cRLSign" \
    -out "${ca_certificate}"

  openssl genpkey \
    -algorithm RSA \
    -pkeyopt rsa_keygen_bits:2048 \
    -out "${server_key}"
  openssl req \
    -new \
    -sha256 \
    -key "${server_key}" \
    -subj "/CN=seaweedfs" \
    -out "${tls_dir}/server.csr"

  cat > "${tls_dir}/server-cert.ext" <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:seaweedfs,DNS:localhost,DNS:seaweedfs-s3.localhost,IP:127.0.0.1
EOF

  openssl x509 \
    -req \
    -sha256 \
    -days 825 \
    -in "${tls_dir}/server.csr" \
    -CA "${ca_certificate}" \
    -CAkey "${ca_key}" \
    -CAcreateserial \
    -extfile "${tls_dir}/server-cert.ext" \
    -out "${server_certificate}"

  rm -f \
    "${tls_dir}/ca.srl" \
    "${tls_dir}/server.csr" \
    "${tls_dir}/server-cert.ext"
fi

chown seaweed:seaweed "${ca_certificate}" "${ca_key}" "${server_certificate}" "${server_key}"
chmod 600 "${ca_key}" "${server_key}"
chmod 644 "${ca_certificate}" "${server_certificate}"

exec /entrypoint.sh "$@"
