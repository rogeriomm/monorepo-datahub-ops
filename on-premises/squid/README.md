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
