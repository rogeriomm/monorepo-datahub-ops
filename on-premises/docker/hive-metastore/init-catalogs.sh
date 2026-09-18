#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

hive_home=${HIVE_HOME:-/opt/hive}
hive_conf_dir=${hive_home}/conf
custom_conf_dir=${HIVE_CUSTOM_CONF_DIR:-/etc/hive/postgres/conf}
db_driver=${DB_DRIVER:-postgres}

find "${custom_conf_dir}" -type f -exec ln -sfn {} "${hive_conf_dir}"/ \;
export HADOOP_CONF_DIR=${hive_conf_dir}
export HIVE_CONF_DIR=${hive_conf_dir}

create_catalog() {
  local catalog_name=$1
  local catalog_location=$2
  local catalog_description=$3

  "${hive_home}/bin/schematool" \
    -dbType "${db_driver}" \
    -createCatalog "${catalog_name}" \
    -catalogLocation "${catalog_location}" \
    -catalogDescription "${catalog_description}" \
    -ifNotExists

  "${hive_home}/bin/schematool" \
    -dbType "${db_driver}" \
    -alterCatalog "${catalog_name}" \
    -catalogLocation "${catalog_location}" \
    -catalogDescription "${catalog_description}"
}

create_catalog iceberg s3a://iceberg-lakehouse 'Iceberg warehouse'
create_catalog delta s3a://delta-lakehouse 'Delta Lake warehouse'
