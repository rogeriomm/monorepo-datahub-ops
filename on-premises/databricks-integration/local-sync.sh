#!/usr/bin/env bash

set -euo pipefail

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
on_premises_directory="$(dirname "$script_directory")"

source "$script_directory/databricks-dab-lib.sh"

cd "$on_premises_directory"

certificate_volume="dbfs:/Volumes/workspace/default/on_premises_certificates"

copy_docker_volume_secret \
  "docker/postgres/certificates/postgres-password" \
  "$certificate_volume/postgres"
copy_docker_volume_secret \
  "docker/postgres/certificates/client-password" \
  "$certificate_volume/postgres"
copy_docker_volume_files \
  "docker/postgres/certificates" \
  "$certificate_volume/postgres" \
  ca.crt postgres-client.p12 client.crt client.key

copy_docker_volume_secret \
  "docker/trino/certificates/client-password" \
  "$certificate_volume/trino"
copy_docker_volume_files \
  "docker/trino/certificates" \
  "$certificate_volume/trino" \
  ca.crt trino-client.p12

copy_docker_volume_files \
  "docker/seaweedfs/certificates" \
  "$certificate_volume/seaweedfs" \
  ca.crt

copy_docker_volume_files \
  "docker/kafka-4/certificates" \
  "$certificate_volume/kafka-4" \
  ca.crt
