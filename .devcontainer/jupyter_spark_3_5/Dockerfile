ARG BASE_IMAGE=local/jupyter-pyspark-base:3.5.3
FROM ${BASE_IMAGE}

ARG SCALA_VERSION=2.12.20

USER root

# Install tools required to download Coursier.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        curl \
        gzip \
    && rm -rf /var/lib/apt/lists/*

# Install Coursier.
RUN curl --fail --location \
        https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux.gz \
        --output /tmp/cs.gz \
    && gzip --decompress /tmp/cs.gz \
    && install -m 0755 /tmp/cs /usr/local/bin/cs \
    && rm -f /tmp/cs

# Almond should be installed as jovyan so its kernel is placed in the
# Jupyter user's kernel directory.
USER ${NB_UID}

RUN cs launch --use-bootstrap almond \
        --scala ${SCALA_VERSION} \
        -- \
        --install \
        --force

# Ensure Spark and Java are visible from the Scala kernel.
ENV SPARK_HOME=/usr/local/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"

WORKDIR "${HOME}/work"
