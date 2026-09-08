ARG HIVE_VERSION=4.2.1
FROM apache/hive:${HIVE_VERSION}

ARG POSTGRES_JDBC_VERSION=42.7.13
USER root
RUN curl --fail --silent --show-error --location \
      "https://repo.maven.apache.org/maven2/org/postgresql/postgresql/${POSTGRES_JDBC_VERSION}/postgresql-${POSTGRES_JDBC_VERSION}.jar" \
      --output /opt/hive/lib/postgres.jar \
    && chmod 644 /opt/hive/lib/postgres.jar

# The upstream entrypoint renders this template before loading custom config.
COPY core-site.xml /opt/hive/conf/core-site.xml.template
USER hive
