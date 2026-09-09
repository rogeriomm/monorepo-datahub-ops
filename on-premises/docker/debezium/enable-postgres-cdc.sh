#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

usage() {
  cat <<'USAGE'
Usage:
  enable-postgres-cdc.sh enable  DATABASE [SCHEMA]
  enable-postgres-cdc.sh disable DATABASE [SCHEMA]

SCHEMA defaults to public. The script changes PostgreSQL and Kafka Connect
runtime state only; it does not edit docker-compose.yaml. Disabling removes the
connector, its stored offsets, replication slot, and publication. Kafka topics
and captured records are retained.

Run this script inside the Compose tools container. The repository must be bind
mounted into the container and the Docker socket must be available.

Optional identity overrides:
  CDC_CONNECTOR_NAME
  CDC_TOPIC_PREFIX
  CDC_SLOT_NAME
  CDC_PUBLICATION_NAME

Optional Compose container-name overrides:
  CDC_POSTGRES_CONTAINER
  CDC_KAFKA_CONTAINER
  CDC_DEBEZIUM_CONTAINER
USAGE
}

if [[ "${1:-}" == --help || "${1:-}" == -h ]]; then
  usage
  exit 0
fi
if (( $# < 2 || $# > 3 )); then
  usage >&2
  exit 64
fi

action=$1
database=$2
schema=${3:-${CDC_SCHEMA:-public}}
if [[ "${action}" != enable && "${action}" != disable ]]; then
  printf 'Action must be enable or disable: %s\n' "${action}" >&2
  usage >&2
  exit 64
fi
if [[ -z "${database}" ]]; then
  printf 'DATABASE must not be empty.\n' >&2
  exit 64
fi

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

if [[ ! -f /.dockerenv && ! -f /run/.containerenv ]]; then
  printf 'This script must be run inside a container such as tools.\n' >&2
  exit 1
fi

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Required command is unavailable: %s\n' "$1" >&2
    exit 1
  fi
}

require_postgres_identifier() {
  local name=$1 value=$2
  if [[ ! "${value}" =~ ^[a-z_][a-z0-9_]{0,62}$ ]]; then
    printf '%s must be a lowercase PostgreSQL identifier: %s\n' \
      "${name}" "${value}" >&2
    exit 1
  fi
}

require_command docker
require_command sed
require_command sha256sum
require_postgres_identifier SCHEMA "${schema}"

if command -v jq >/dev/null 2>&1; then
  jq_command=(jq)
elif command -v mise >/dev/null 2>&1 \
  && jq_path=$(mise which jq 2>/dev/null) \
  && [[ -x "${jq_path}" ]]; then
  jq_command=("${jq_path}")
else
  printf 'Required command is unavailable: jq\n' >&2
  exit 1
fi

json_query() {
  "${jq_command[@]}" "$@"
}

postgres_container=${CDC_POSTGRES_CONTAINER:-postgres}
kafka_container=${CDC_KAFKA_CONTAINER:-kafka-4}
debezium_container=${CDC_DEBEZIUM_CONTAINER:-debezium}

require_container() {
  if ! docker container inspect "$1" >/dev/null 2>&1; then
    printf 'Required Compose container does not exist: %s\n' "$1" >&2
    printf 'Create the CDC stack before running this script.\n' >&2
    exit 1
  fi
}

start_container() {
  local container=$1
  if [[ $(docker container inspect --format '{{.State.Running}}' "${container}") != true ]]; then
    docker container start "${container}" >/dev/null
  fi
}

wait_for_container() {
  local container=$1 state
  for _attempt in {1..60}; do
    state=$(docker container inspect --format \
      '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' \
      "${container}")
    if [[ "${state}" == healthy || "${state}" == running ]]; then
      return
    fi
    if [[ "${state}" == unhealthy || "${state}" == exited || "${state}" == dead ]]; then
      printf 'Container %s entered state %s.\n' "${container}" "${state}" >&2
      exit 1
    fi
    sleep 2
  done
  printf 'Timed out waiting for container %s.\n' "${container}" >&2
  exit 1
}

require_container "${postgres_container}"
require_container "${kafka_container}"
require_container "${debezium_container}"

# Preserve short, readable names for conventional lowercase databases. Add a
# hash when normalization or a non-public schema could otherwise cause a name
# collision.
resource_slug=$(printf '%s' "${database}" | LC_ALL=C sed \
  -e 's/[^A-Za-z0-9][^A-Za-z0-9]*/_/g' \
  -e 's/^_*//' \
  -e 's/_*$//' \
  -e 's/.*/\L&/')
resource_slug=${resource_slug:0:32}
resource_slug=${resource_slug:-database}
resource_hash=$(printf '%s/%s' "${database}" "${schema}" | sha256sum)
resource_hash=${resource_hash%% *}
resource_hash=${resource_hash:0:8}

if [[ "${database}" =~ ^[a-z_][a-z0-9_]{0,31}$ && "${schema}" == public ]]; then
  resource_id=${database}
else
  resource_id=${resource_slug}_${resource_hash}
fi
connector_slug=${resource_id//_/-}

connector_name=${CDC_CONNECTOR_NAME:-${connector_slug}-postgres}
topic_prefix=${CDC_TOPIC_PREFIX:-${connector_slug}}
slot_name=${CDC_SLOT_NAME:-dbz_${resource_id}}
publication_name=${CDC_PUBLICATION_NAME:-dbz_${resource_id}_publication}

require_postgres_identifier CDC_SLOT_NAME "${slot_name}"
require_postgres_identifier CDC_PUBLICATION_NAME "${publication_name}"
if [[ ! "${connector_name}" =~ ^[A-Za-z0-9._-]+$ ]]; then
  printf 'Invalid CDC_CONNECTOR_NAME: %s\n' "${connector_name}" >&2
  exit 1
fi
if [[ ! "${topic_prefix}" =~ ^[A-Za-z0-9._-]+$ ]]; then
  printf 'Invalid CDC_TOPIC_PREFIX: %s\n' "${topic_prefix}" >&2
  exit 1
fi

connect_curl() {
  docker container exec --interactive "${debezium_container}" \
    curl --silent --show-error "$@"
}

connector_status() {
  connect_curl --fail --max-time 10 \
    "http://localhost:8083/connectors/${connector_name}/status"
}

start_container "${postgres_container}"
start_container "${kafka_container}"
wait_for_container "${postgres_container}"
wait_for_container "${kafka_container}"

database_exists=$(docker container exec --interactive \
  -e CDC_DATABASE="${database}" \
  "${postgres_container}" bash -c \
  'psql -X --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --no-psqlrc --no-align --tuples-only --set=ON_ERROR_STOP=1' <<'SQL'
\getenv cdc_database CDC_DATABASE
SELECT EXISTS (SELECT FROM pg_database WHERE datname = :'cdc_database');
SQL
)
if [[ "${database_exists}" != t ]]; then
  printf 'PostgreSQL database does not exist: %s\n' "${database}" >&2
  exit 1
fi

if [[ "${action}" == enable ]]; then
  postgres_image=$(docker container inspect --format '{{.Config.Image}}' \
    "${postgres_container}")
  config_volume=$(docker container inspect --format \
    '{{range .Mounts}}{{if eq .Destination "/etc/debezium/postgres"}}{{.Name}}{{end}}{{end}}' \
    "${debezium_container}")
  if [[ -z "${config_volume}" ]]; then
    printf 'Container %s has no named volume at /etc/debezium/postgres.\n' \
      "${debezium_container}" >&2
    exit 1
  fi

  init_env_file=$(mktemp)
  trap 'rm -f "${init_env_file}"' EXIT
  chmod 600 "${init_env_file}"
  docker container inspect --format '{{range .Config.Env}}{{println .}}{{end}}' \
    "${postgres_container}" \
    | sed -n \
      -e '/^POSTGRES_USER=/p' \
      -e '/^POSTGRES_PASSWORD=/p' \
      -e '/^POSTGRES_MTLS_ENABLED=/p' \
      > "${init_env_file}"
  {
    printf 'POSTGRES_DB=%s\n' "${database}"
    printf 'DEBEZIUM_SCHEMA=%s\n' "${schema}"
    printf 'DEBEZIUM_PUBLICATION_NAME=%s\n' "${publication_name}"
  } >> "${init_env_file}"

  docker container run --rm --interactive \
    --security-opt label=disable \
    --network "container:${postgres_container}" \
    --volumes-from "${postgres_container}:ro" \
    --mount "type=volume,src=${config_volume},dst=/etc/debezium/postgres" \
    --env-file "${init_env_file}" \
    --entrypoint /bin/bash \
    "${postgres_image}" -s < "${script_dir}/init-postgres.sh"

  rm -f "${init_env_file}"
  trap - EXIT

  start_container "${debezium_container}"
  wait_for_container "${debezium_container}"

  schema_filter="\\Q${schema}\\E"
  connector_config=$(json_query --null-input --compact-output \
    --arg database "${database}" \
    --arg schema_filter "${schema_filter}" \
    --arg topic_prefix "${topic_prefix}" \
    --arg slot_name "${slot_name}" \
    --arg publication_name "${publication_name}" \
    '{
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "tasks.max": "1",
      "database.hostname": "postgres",
      "database.port": "5432",
      "database.user": "debezium",
      "database.password": "${file:/etc/debezium/postgres/credentials.properties:password}",
      "database.dbname": $database,
      "database.sslmode": "verify-full",
      "database.sslrootcert": "/etc/debezium/postgres/ca.crt",
      "database.sslkey": "/etc/debezium/postgres/debezium.p12",
      "database.sslpassword": "",
      "plugin.name": "pgoutput",
      "slot.name": $slot_name,
      "slot.drop.on.stop": "false",
      "publication.name": $publication_name,
      "publication.autocreate.mode": "disabled",
      "schema.include.list": $schema_filter,
      "topic.prefix": $topic_prefix,
      "snapshot.mode": "initial",
      "heartbeat.interval.ms": "10000",
      "topic.creation.default.replication.factor": "1",
      "topic.creation.default.partitions": "3",
      "key.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "key.converter.schemas.enable": "false",
      "value.converter.schemas.enable": "false"
    }')

  printf '%s' "${connector_config}" | connect_curl \
    --fail \
    --request PUT \
    --header 'Content-Type: application/json' \
    --data-binary @- \
    "http://localhost:8083/connectors/${connector_name}/config" \
    >/dev/null

  status='{}'
  for _attempt in {1..60}; do
    if status=$(connector_status 2>/dev/null) \
      && json_query --exit-status \
        '.connector.state == "RUNNING"
         and (.tasks | length) > 0
         and all(.tasks[]; .state == "RUNNING")' \
        <<<"${status}" >/dev/null; then
      json_query . <<<"${status}"
      printf 'CDC enabled for database %s, schema %s.\n' \
        "${database}" "${schema}"
      printf 'Kafka topics use prefix %s.%s.\n' \
        "${topic_prefix}" "${schema}"
      exit 0
    fi

    if json_query --exit-status \
      '.connector.state == "FAILED" or any(.tasks[]; .state == "FAILED")' \
      <<<"${status}" >/dev/null 2>&1; then
      printf 'Debezium connector failed:\n%s\n' "${status}" >&2
      exit 1
    fi
    sleep 2
  done

  printf 'Timed out waiting for Debezium connector %s:\n%s\n' \
    "${connector_name}" "${status}" >&2
  exit 1
fi

# Disable: stop and reset the connector before removing it. Resetting offsets is
# required because the replication slot is dropped below; a later enable then
# performs a clean initial snapshot instead of referring to an obsolete LSN.
start_container "${debezium_container}"
wait_for_container "${debezium_container}"

if connect_curl --fail --output /dev/null \
  "http://localhost:8083/connectors/${connector_name}/config" 2>/dev/null; then
  connect_curl --fail --request PUT --output /dev/null \
    "http://localhost:8083/connectors/${connector_name}/stop"

  stopped=false
  for _attempt in {1..30}; do
    status=$(connector_status 2>/dev/null || true)
    status=${status:-'{}'}
    if [[ $(json_query --raw-output '.connector.state // empty' <<<"${status}") == STOPPED ]]; then
      stopped=true
      break
    fi
    sleep 1
  done
  if [[ "${stopped}" != true ]]; then
    printf 'Timed out stopping connector %s.\n' "${connector_name}" >&2
    exit 1
  fi

  connect_curl --fail --request DELETE --output /dev/null \
    "http://localhost:8083/connectors/${connector_name}/offsets"
  connect_curl --fail --request DELETE --output /dev/null \
    "http://localhost:8083/connectors/${connector_name}"

  for _attempt in {1..30}; do
    if ! connect_curl --fail --output /dev/null \
      "http://localhost:8083/connectors/${connector_name}/config" 2>/dev/null; then
      break
    fi
    sleep 1
  done
else
  printf 'Connector %s is already absent.\n' "${connector_name}"
fi

slot_state=active
for _attempt in {1..30}; do
  slot_state=$(docker container exec --interactive \
    -e PGDATABASE="${database}" \
    -e CDC_SLOT="${slot_name}" \
    "${postgres_container}" bash -c \
    'psql -X --username="$POSTGRES_USER" --no-psqlrc --no-align --tuples-only --set=ON_ERROR_STOP=1' <<'SQL'
\getenv cdc_slot CDC_SLOT
SELECT COALESCE(
  (SELECT active::text FROM pg_replication_slots WHERE slot_name = :'cdc_slot'),
  'missing'
);
SQL
  )
  if [[ "${slot_state}" != true ]]; then
    break
  fi
  sleep 1
done
if [[ "${slot_state}" == true ]]; then
  printf 'Replication slot is still active: %s\n' "${slot_name}" >&2
  exit 1
fi

docker container exec --interactive \
  -e PGDATABASE="${database}" \
  -e CDC_SLOT="${slot_name}" \
  -e CDC_PUBLICATION="${publication_name}" \
  "${postgres_container}" bash -c \
  'psql -X --username="$POSTGRES_USER" --no-psqlrc --set=ON_ERROR_STOP=1' <<'SQL'
\getenv cdc_slot CDC_SLOT
\getenv cdc_publication CDC_PUBLICATION
SELECT pg_drop_replication_slot(:'cdc_slot')
WHERE EXISTS (
  SELECT FROM pg_replication_slots WHERE slot_name = :'cdc_slot'
);
SELECT format('DROP PUBLICATION %I', :'cdc_publication')
WHERE EXISTS (
  SELECT FROM pg_publication WHERE pubname = :'cdc_publication'
)
\gexec
SQL

printf 'CDC disabled for database %s, schema %s.\n' "${database}" "${schema}"
printf 'Kafka topics with prefix %s.%s were retained.\n' \
  "${topic_prefix}" "${schema}"
