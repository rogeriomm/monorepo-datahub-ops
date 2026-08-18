#!/usr/bin/env zsh

set -euo pipefail

project_dir=${0:A:h}
cd "$project_dir"

rm -rf -- \
  "$project_dir/build" \
  "$project_dir/dist/squid-databricks" \
  "$project_dir/dist/squid-on-premises" \
  "$project_dir/packages/build" \
  "$project_dir/packages/squid-databricks/build" \
  "$project_dir/packages/squid-on-premises/build"

build_wheel() {
  local source_dir=$1
  local python_version=$2
  local output_dir=$3
  local python_tag=${python_version//./}

  uv run \
    --with build \
    --no-project \
    --python "$python_version" \
    -- \
    python -m build \
    --wheel \
    --outdir "$output_dir" \
    "--config-setting=--build-option=--python-tag=py$python_tag" \
    "$source_dir"
}

local_python_versions=(3.11 3.12 3.13)

for python_version in $local_python_versions; do
  build_wheel packages/squid-on-premises "$python_version" dist/squid-on-premises
  build_wheel . "$python_version" dist/squid-local
done

build_wheel packages/squid-databricks 3.12 dist/squid-databricks
