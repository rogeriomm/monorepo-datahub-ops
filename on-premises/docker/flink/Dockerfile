ARG FLINK_VERSION=2.1.3
ARG SCALA_VERSION=2.12
ARG JAVA_VERSION=17

FROM eclipse-temurin:17-jdk-jammy AS delta-builder

ARG DELTA_VERSION=4.4.0
ARG DELTA_SOURCE_SHA256=4d343764371e3882749cbad52c335bca707f79efe7f65b51a0155364a793ee19
ARG FLINK_VERSION=2.1.3

RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src/delta

COPY delta-seaweedfs.patch /tmp/delta-seaweedfs.patch

RUN curl --fail --location --silent --show-error \
        "https://github.com/delta-io/delta/archive/refs/tags/v${DELTA_VERSION}.tar.gz" \
        --output /tmp/delta.tar.gz \
    && echo "${DELTA_SOURCE_SHA256}  /tmp/delta.tar.gz" | sha256sum --check \
    && tar --extract --gzip --strip-components=1 --file=/tmp/delta.tar.gz \
    && git apply /tmp/delta-seaweedfs.patch \
    && ./build/sbt -batch -no-colors -DflinkVersion="${FLINK_VERSION}" flink/assembly \
    && install --mode=0644 \
        "flink/target/delta-flink-${FLINK_VERSION}-${DELTA_VERSION}.jar" \
        /tmp/delta-flink.jar

FROM flink:${FLINK_VERSION}-scala_${SCALA_VERSION}-java${JAVA_VERSION}

ARG AWS_SDK_VERSION=2.23.19
ARG FLINK_KAFKA_CONNECTOR_VERSION=5.0.0-2.1
ARG GUAVA_VERSION=33.5.0-jre

USER root

COPY --from=delta-builder /tmp/delta-flink.jar /opt/flink/lib/delta-flink.jar

RUN curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/${FLINK_KAFKA_CONNECTOR_VERSION}/flink-sql-connector-kafka-${FLINK_KAFKA_CONNECTOR_VERSION}.jar" \
        --output /opt/flink/lib/flink-sql-connector-kafka.jar \
    && curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_VERSION}/bundle-${AWS_SDK_VERSION}.jar" \
        --output /opt/flink/lib/aws-sdk-bundle.jar \
    && curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/com/google/guava/guava/${GUAVA_VERSION}/guava-${GUAVA_VERSION}.jar" \
        --output /opt/flink/lib/guava.jar \
    && chown flink:flink \
        /opt/flink/lib/aws-sdk-bundle.jar \
        /opt/flink/lib/delta-flink.jar \
        /opt/flink/lib/flink-sql-connector-kafka.jar \
        /opt/flink/lib/guava.jar

COPY --chown=flink:flink core-site.xml /opt/flink/conf/core-site.xml
COPY --chown=flink:flink delta-flink.properties /opt/flink/conf/delta-flink.properties
COPY --chown=flink:flink kafka-debezium-to-delta.sql /opt/flink/examples/kafka-debezium-to-delta.sql

USER flink
