#!/usr/bin/env zsh

set -euo pipefail

playbook="./playbooks/upgrade.yml"

cmd=(
  ansible-playbook
  "$playbook"
  -K
  -e "github_token=${GITHUB_TOKEN:-}"
)

if (( $# > 0 )); then
  cmd+=("$@")
fi

"${cmd[@]}"

