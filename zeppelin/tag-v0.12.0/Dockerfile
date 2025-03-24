FROM openjdk:11 as builder
ADD . /workspace/zeppelin
WORKDIR /workspace/zeppelin
ENV MAVEN_OPTS="-Xms1024M -Xmx2048M -XX:MaxMetaspaceSize=1024m -XX:-UseGCOverheadLimit -Dorg.slf4j.simpleLogger.log.org.apache.maven.cli.transfer.Slf4jMavenTransferListener=warn"
ENV MAVEN_PARMS="-B -DskipTests -Pbuild-distr -Pspark-3.5 -Pinclude-hadoop -Pspark-scala-2.12 -Pweb-classic -Pweb-dist"

# Allow npm and bower to run with root privileges
RUN --mount=type=cache,target=/root/.m2 \
    echo "unsafe-perm=true" > ~/.npmrc && \
    echo '{ "allow_root": true }' > ~/.bowerrc && \
    ./mvnw -B package ${MAVEN_PARMS} && \
    mv /workspace/zeppelin/zeppelin-distribution/target/zeppelin-*-bin/zeppelin-*-bin /opt/zeppelin/ && \
    # Removing stuff saves time, because docker creates a temporary layer
    rm -rf /workspace/zeppelin/*

FROM ubuntu:22.04
COPY --from=builder /opt/zeppelin /opt/zeppelin
