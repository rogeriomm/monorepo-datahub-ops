ARG SUPERSET_VERSION=6.1.0
FROM apache/superset:${SUPERSET_VERSION}

USER root

RUN /app/docker/apt-install.sh \
    default-libmysqlclient-dev \
    pkg-config

RUN /app/docker/pip-install.sh --requires-build-essential --no-cache \
    ".[athena,bigquery,databricks,mssql,mysql,redshift,snowflake,spark,trino, duckdb,mongodb]"

USER superset
