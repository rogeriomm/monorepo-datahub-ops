#!/usr/bin/env zsh

set -euo pipefail

fig() {
    if command -v toilet >/dev/null 2>&1; then
        toilet "$@"
    elif command -v figlet >/dev/null 2>&1; then
        figlet -w 132 "$@"
    else
        echo "$*"
    fi
}

db_wp() {
  databricks workspace "$@"
}

export_dir_as_jupyter() {
  local remote_dir="$1"
  local local_dir="$2"
  local objects object_type object_path object_name

  mkdir -p "$local_dir"
  objects="$(db_wp list "$remote_dir" -o json)"

  while IFS=$'\t' read -r object_type object_path; do
    object_name="${object_path##*/}"

    case "$object_type" in
      DIRECTORY)
        export_dir_as_jupyter "$object_path" "$local_dir/$object_name"
        ;;
      NOTEBOOK)
        [[ "$object_name" == *.ipynb ]] || object_name="${object_name}.ipynb"
        db_wp export \
          "$object_path" \
          --format JUPYTER \
          --file "$local_dir/$object_name"
        ;;
    esac
  done < <(jq -r '.[] | [.object_type, .path] | @tsv' <<< "$objects")
}

DATABRICKS_USER="rogermm@gmail.com"
BASE_LOCAL_REPO="$(basename "$(git rev-parse --show-toplevel)")"
BASE_DIR="/Users/$DATABRICKS_USER/$BASE_LOCAL_REPO"
REMOTE_NOTEBOOKS="$BASE_DIR/notebooks/jupyter/databricks/free-edition"

# Absolute path of the directory containing this script.
# ${0:A} converts the script path to an absolute path.
# :h removes the script filename, leaving its parent directory.
LOCAL_NOTEBOOKS="${0:A:h}"

command -v jq >/dev/null 2>&1 || {
  print -u2 "jq is required to export the workspace recursively"
  exit 1
}

fig "Databricks  notebook  sync"

databricks auth describe

export_dir_as_jupyter "$REMOTE_NOTEBOOKS" "$LOCAL_NOTEBOOKS"
