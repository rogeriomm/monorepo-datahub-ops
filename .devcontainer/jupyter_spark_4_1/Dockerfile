ARG BASE_IMAGE=local/jupyter-pyspark-base:4.1.2
FROM ${BASE_IMAGE}

ARG SCALA_VERSION=2.13.17

USER root

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        curl \
        gzip \
        build-essential \
        libpq-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl --fail --location \
        https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux.gz \
        --output /tmp/cs.gz \
    && gzip --decompress /tmp/cs.gz \
    && install -m 0755 /tmp/cs /usr/local/bin/cs \
    && rm -f /tmp/cs

RUN pip install --no-cache-dir \
    pandas parquet-tools kagglehub contexttimer rich findspark \
    humanize ipython-autotime

RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/jovyan \
  && chmod 0440 /etc/sudoers.d/jovyan

USER ${NB_UID}

RUN cs launch --use-bootstrap almond \
        --scala ${SCALA_VERSION} \
        -- \
        --install \
        --force

# Disable JupyterLab announcements inside the container.
RUN jupyter labextension disable \
    "@jupyterlab/apputils-extension:announcements" \
    --level=sys_prefix

USER root

COPY jupyterlab-overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json

ENV SPARK_HOME=/usr/local/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"

USER ${NB_UID}

WORKDIR "${HOME}/work"
