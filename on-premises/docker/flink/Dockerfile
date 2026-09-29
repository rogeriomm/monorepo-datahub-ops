ARG FLINK_VERSION=2.1.3
ARG SCALA_VERSION=2.12
ARG JAVA_VERSION=17

FROM flink:${FLINK_VERSION}-scala_${SCALA_VERSION}-java${JAVA_VERSION}

ARG FLINK_KAFKA_CONNECTOR_VERSION=5.0.0-2.1
ARG FLINK_KAFKA_CONNECTOR_SHA256=11cbbcd1163c4fae0d23f9e2c55b4ff57a719a39fe96fc780001cd21a4e5ba15
ARG FLINK_SHADED_HADOOP_VERSION=2.8.3-10.0
ARG FLINK_SHADED_HADOOP_SHA256=492b2a559f2a1dad3808b51d9a26a575dbb1202004c9f85f5059c520e0632127
ARG ICEBERG_VERSION=1.11.0
ARG ICEBERG_FLINK_RUNTIME_SHA256=39e658d876f253815b4b17c6676bebf6a24d517afe93a21298106d1d7fa97331
ARG ICEBERG_AWS_BUNDLE_SHA256=38f01da7e96850cdd05e6616d758b77b43314b712a8808e3f9a824d56976162f

USER root

RUN curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/${FLINK_KAFKA_CONNECTOR_VERSION}/flink-sql-connector-kafka-${FLINK_KAFKA_CONNECTOR_VERSION}.jar" \
        --output /opt/flink/lib/flink-sql-connector-kafka.jar \
    && curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/${FLINK_SHADED_HADOOP_VERSION}/flink-shaded-hadoop-2-uber-${FLINK_SHADED_HADOOP_VERSION}.jar" \
        --output /opt/flink/lib/flink-shaded-hadoop-2-uber.jar \
    && curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/org/apache/iceberg/iceberg-flink-runtime-2.1/${ICEBERG_VERSION}/iceberg-flink-runtime-2.1-${ICEBERG_VERSION}.jar" \
        --output /opt/flink/lib/iceberg-flink-runtime.jar \
    && curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar" \
        --output /opt/flink/lib/iceberg-aws-bundle.jar \
    && printf '%s  %s\n' \
        "${FLINK_KAFKA_CONNECTOR_SHA256}" /opt/flink/lib/flink-sql-connector-kafka.jar \
        "${FLINK_SHADED_HADOOP_SHA256}" /opt/flink/lib/flink-shaded-hadoop-2-uber.jar \
        "${ICEBERG_FLINK_RUNTIME_SHA256}" /opt/flink/lib/iceberg-flink-runtime.jar \
        "${ICEBERG_AWS_BUNDLE_SHA256}" /opt/flink/lib/iceberg-aws-bundle.jar \
        | sha256sum --check \
    && chown flink:flink \
        /opt/flink/lib/flink-sql-connector-kafka.jar \
        /opt/flink/lib/flink-shaded-hadoop-2-uber.jar \
        /opt/flink/lib/iceberg-flink-runtime.jar \
        /opt/flink/lib/iceberg-aws-bundle.jar

COPY --chown=flink:flink kafka-debezium-to-iceberg.sql /opt/flink/examples/kafka-debezium-to-iceberg.sql

USER flink
