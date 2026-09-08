#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

# PUT creates or updates the same connector without resetting its offsets.
curl --fail --silent --show-error \
  --retry 12 --retry-all-errors --retry-delay 5 --max-time 30 \
  --request PUT --header 'Content-Type: application/json' \
  --data-binary @/etc/debezium/postgres-connector.json \
  --output /dev/null \
  http://debezium:8083/connectors/compose-postgres/config

# The REST API can accept a configuration before its task fails. Wait for both.
for attempt in {1..60}; do
  # Status may return 404 briefly while the worker assigns the new connector.
  if ! status=$(curl --fail --silent --show-error --max-time 10 \
    http://debezium:8083/connectors/compose-postgres/status); then
    sleep 2
    continue
  fi
  if [[ "${status}" == *'"state":"FAILED"'* ]]; then
    printf 'Debezium connector failed: %s\n' "${status}" >&2
    exit 1
  fi
  running_count=$(printf '%s' "${status}" | grep -o '"state":"RUNNING"' | wc -l || true)
  if (( running_count == 2 )); then
    echo 'Debezium compose-postgres connector and task are RUNNING.'
    exit 0
  fi
  sleep 2
done

printf 'Timed out waiting for Debezium: %s\n' "${status}" >&2
exit 1
