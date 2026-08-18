#!/usr/bin/env bash

set -eu

copy_databricks() {
  certificate_path="$1"
  volume="$2"

  shift 2
  files="$@"

  volume_local="${volume#dbfs:}"
  docker_volume_local="docker$volume_local"

  mkdir -p $docker_volume_local

  echo "$docker_volume_local"

  echo "Copy Databricks volume $volume from $certificate_path files: $files"

  databricks fs mkdir $volume

  for certificate in "$@"; do
    cf="$certificate_path/$certificate"

    if [ ! -s "$cf" ]; then
      echo "Missing TLS file: $cf" >&2
      exit 1
    fi

    # Copy the file in the local Docker container /Volume directory to mimic the Databricks environment
    cp "$cf" "$docker_volume_local/"

    # Copy the file to the /Volume directory
    databricks fs cp \
            "$cf" \
            "$volume/$certificate" \
            --overwrite
  done
}

copy_databricks_secret() {
  source="$1"
  volume=$2
  password_file="$3"
  scope="$4"
  key="$5"

  volume_local="${volume#dbfs:}"
  docker_volume_local="docker$volume_local"

  echo "Copy secret_file: $password_file scope: $scope key: $key"

  if [ ! -s "$password_file" ]; then
    echo "Skipping PostgreSQL password secret: $password_file does not exist"
    exit 0
  fi

  # Copy the file in the local Docker container /Volume directory to mimic the Databricks environment
  mkdir -p "$docker_volume_local"
  cp "$password_file" "$docker_volume_local/secret-$(basename "$password_file")"

  databricks secrets put-secret \
     "$scope" \
     $key \
    < "$password_file"
}

copy_databricks_secret_from_env() {
  local variable_name="$1"
  local scope="$2"
  local key="$3"
  local env_file="${4:-docker/.env}"
  local value

  if [[ ! "$variable_name" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
    echo "Invalid credential variable name: $variable_name" >&2
    return 1
  fi

  if [[ ! -f "$env_file" ]]; then
    echo "Missing Docker Compose environment file: $env_file" >&2
    return 1
  fi

  value=$(sed -n "s/^${variable_name}=//p" "$env_file")
  if [[ -z "$value" ]]; then
    echo "Missing credential $variable_name in $env_file" >&2
    return 1
  fi

  printf '%s' "$value" | databricks secrets put-secret \
    "$scope" \
    "$key"
}

copy_squid_wheel_to_docker() {
  cp ./squid/dist/squid-on-premises/*.whl docker/Volumes/workspace/default/on_premises_artifacts/python-wheels
}

upload_squid_wheel_to_volume() {
  local squid_source="$1"
  local squid_wheel_volume="$2"
  local wheel_pattern="$3"
  local wheel_count=0
  local wheel_name
  local wheel_path

  if ! command -v uv >/dev/null 2>&1; then
    echo "The uv command is required to build the Squid wheel" >&2
    return 1
  fi

  if [[ ! -f "$squid_source/packages/squid-on-premises/pyproject.toml" ]]; then
    echo "Missing Python project: $squid_source/packages/squid-on-premises/pyproject.toml" >&2
    return 1
  fi

  (
    cd "$squid_source"
    ./build-wheel.sh
  )

  volume_local="${squid_wheel_volume#dbfs:}"
  docker_volume_local="docker$volume_local"
  mkdir -p $docker_volume_local

  databricks fs mkdir "$squid_wheel_volume"

  while IFS= read -r -d '' wheel_path; do
    wheel_name=$(basename "$wheel_path")
    databricks fs cp \
      "$wheel_path" \
      "$squid_wheel_volume/$wheel_name" \
      --overwrite
    cp "$wheel_path" $docker_volume_local
    wheel_count=$((wheel_count + 1))
  done < <(
    find "$squid_source/dist" \
      -maxdepth 2 \
      -type f \
      -name "$wheel_pattern" \
      -size +0c \
      -print0
  )

  if (( wheel_count == 0 )); then
    echo "No Python wheel matching $wheel_pattern was built in $squid_source/dist" >&2
    return 1
  fi
}
