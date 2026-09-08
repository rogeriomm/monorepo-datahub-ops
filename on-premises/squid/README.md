# Squid packages

The uv workspace contains a local development project and two deployable
distributions with separate dependencies. `squid-on-premises` supports Python
3.11, 3.12, and 3.13, while `squid-databricks` targets the Python 3.12 runtime
used by Databricks Free Edition.

The `squid-local` manifest in the Squid root defines the PyCharm development
environment and the shared uv workspace. Deployment package manifests live in
`packages/squid-on-premises` and `packages/squid-databricks`.

| Project | Purpose | Dependencies |
| --- | --- | --- |
| `squid-local` | PyCharm and local development | On-premises dependencies and Jupyter kernel support |
| `squid-on-premises` | On-premises deployment wheel | dbt Core, PostgreSQL, and terminal utilities |
| `squid-databricks` | Databricks deployment wheel | Databricks SDK, dbt adapter, and PostgreSQL |

Both deployment distributions use version `0.1.0` and provide the `squid`
Python package.

## Spark metastore

`squid.spark.session.get_spark()` uses the Compose Hive Metastore at
`thrift://hive-metastore:9083` and the shared `s3a://trino-lakehouse` warehouse.
Iceberg catalogs use this metastore too. Start the service from
`on-premises/docker` before creating a Spark session:

```shell
docker compose --profile trino up -d --build hive-metastore
```

Run Spark on the Compose `backend` network so it can resolve `hive-metastore`
and `seaweedfs`. Set `HIVE_METASTORE_URI` in the Spark process environment to
override the metastore address. SeaweedFS credentials come from
`SEAWEEDFS_ACCESS_KEY_ID` and `SEAWEEDFS_SECRET_ACCESS_KEY`; Compose passes these
to the Jupyter Spark 3.5, 4.1, and 4.2 services. Storage settings apply only to
the `trino-lakehouse` bucket, preserving AWS access for other buckets.

Restart the notebook kernel after changing session configuration. Existing local
Derby metadata and local warehouse files are not migrated automatically.

Spark uses an isolated Hive client downloaded through Maven (4.0.1 for Spark 4,
3.1.3 for Spark 3). Iceberg additionally loads a checksum-verified Hive 4.0.1
client from `~/.cache/squid/hive-client`, because Spark's bundled Hive 2.3 client
calls RPCs removed from the Compose Hive 4.2 server. Spark 3 Iceberg sessions
also load a compatible Thrift 0.16 library from that cache. The first session requires
network access to Maven repositories and can take several minutes to resolve
dependencies. Later sessions reuse the downloaded dependencies.

## Create the environment

From the repository root:

```shell
cd on-premises/squid-test
uv venv --python 3.12
uv sync --package squid-test-local
```

## Build the wheels

```shell
cd on-premises/squid-test
./build-wheel.sh
```

The build creates three `squid-on-premises` wheels, each using the requested
Python interpreter, and one Python 3.12 `squid-databricks` wheel:

```text
dist/squid-on-premises/squid_on_premises-0.1.0-py311-none-any.whl
dist/squid-on-premises/squid_on_premises-0.1.0-py312-none-any.whl
dist/squid-on-premises/squid_on_premises-0.1.0-py313-none-any.whl
dist/squid-databricks/squid_databricks-0.1.0-py312-none-any.whl
```

Python wheel filenames normalize distribution-name hyphens to underscores.
Their installable distribution names remain `squid-on-premises` and
`squid-databricks`. The `py311`, `py312`, and `py313` compatibility tags record
the Python minor version for each wheel.

## Install and verify

Install the wheel for the target environment. For a Databricks environment:

```shell
cd on-premises/squid-test
uv pip install --python .venv/bin/python --force-reinstall --no-deps \
  dist/squid-test-databricks/squid_databricks-0.1.0-py312-none-any.whl

.venv/bin/python -c "import squid.resources.postgres"
```

For an on-premises environment, select the wheel whose filename tag matches its
Python minor version. Do not install both deployment variants into the same
environment because they provide the same `squid` import packages.

## Run dbt

```shell
uv run --package squid-test-local dbt
```
