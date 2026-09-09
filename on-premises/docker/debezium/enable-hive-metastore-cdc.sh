#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

if (( $# < 1 || $# > 2 )); then
  printf 'Usage: enable-hive-metastore-cdc.sh {enable|disable} [SCHEMA]\n' >&2
  exit 64
fi

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "${script_dir}/enable-postgres-cdc.sh" "$1" hive_metastore "${2:-public}"
