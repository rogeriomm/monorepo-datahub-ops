#!/bin/sh

set -eu

env_file="$(dirname "$0")/../on-premises/docker/.env"

read_setting() {
  setting_name=$1
  setting_value=$(printenv "$setting_name" 2>/dev/null || true)

  if [ -z "$setting_value" ] && [ -r "$env_file" ]; then
    setting_value=$(sed -n "s/^${setting_name}=//p" "$env_file" | sed -n '1p')
  fi

  case "$setting_value" in
    \"*\") setting_value=${setting_value#\"}; setting_value=${setting_value%\"} ;;
    \'*\') setting_value=${setting_value#\'}; setting_value=${setting_value%\'} ;;
  esac

  if [ -z "$setting_value" ]; then
    echo "$setting_name is unset and unavailable in $env_file" >&2
    exit 1
  fi

  printf '%s' "$setting_value"
}

username=$(read_setting TRAEFIK_BASIC_AUTH_USERNAME)
password=$(read_setting TRAEFIK_BASIC_AUTH_PASSWORD)
credentials=$(printf '%s:%s' "$username" "$password" | base64 | tr -d '\n')

printf '{"Authorization":"Basic %s"}\n' "$credentials"
