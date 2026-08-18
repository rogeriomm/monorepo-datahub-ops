#!/bin/sh

set -eu

tls_dir=/etc/seaweedfs/tls
ca_certificate="${tls_dir}/ca.crt"
ca_key="${tls_dir}/ca.key"
server_certificate="${tls_dir}/server.crt"
server_key="${tls_dir}/server.key"
external_hostname=${SEAWEEDFS_HOSTNAME:?SEAWEEDFS_HOSTNAME must be set}

is_valid_hostname() {
  hostname_to_validate=$1
  if [ "${#hostname_to_validate}" -gt 253 ]; then
    return 1
  fi

  case "${hostname_to_validate}" in
    *[!A-Za-z0-9.-]* | .* | *. | *..*) return 1 ;;
  esac

  original_ifs=${IFS}
  IFS=.
  set -- ${hostname_to_validate}
  IFS=${original_ifs}
  for hostname_label in "$@"; do
    if [ "${#hostname_label}" -gt 63 ]; then
      return 1
    fi

    case "${hostname_label}" in
      -* | *-) return 1 ;;
    esac
  done

  return 0
}

if ! is_valid_hostname "${external_hostname}"; then
  echo "Invalid SEAWEEDFS_HOSTNAME: ${external_hostname}" >&2
  exit 1
fi

mkdir -p "${tls_dir}"

regenerate=false
for required_file in "${ca_certificate}" "${ca_key}" "${server_certificate}" "${server_key}"; do
  if [ ! -s "${required_file}" ]; then
    regenerate=true
  fi
done

if [ -s "${server_certificate}" ]; then
  for required_hostname in seaweedfs "${external_hostname}"; do
    if ! openssl x509 \
      -in "${server_certificate}" \
      -noout \
      -checkhost "${required_hostname}" >/dev/null 2>&1; then
      regenerate=true
    fi
  done
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
    -subj "/CN=${external_hostname}" \
    -out "${tls_dir}/server.csr"

  cat > "${tls_dir}/server-cert.ext" <<EOF
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:${external_hostname},DNS:seaweedfs,DNS:localhost,DNS:seaweedfs-s3.localhost,IP:127.0.0.1
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
