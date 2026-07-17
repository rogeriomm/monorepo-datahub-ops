FROM amazon/aws-glue-libs:5

ARG SCALA_VERSION=2.12.18

USER root

RUN curl --fail --location \
        https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux.gz \
        --output /tmp/cs.gz \
    && gzip --decompress /tmp/cs.gz \
    && install -m 0755 /tmp/cs /usr/local/bin/cs \
    && rm -f /tmp/cs

RUN pip install --no-cache-dir \
    pandas parquet-tools kagglehub contexttimer rich findspark jupyterlab

COPY --chown=hadoop:hadoop user-settings/ /home/hadoop/.jupyter/lab/user-settings/
COPY --chown=hadoop:hadoop labconfig/ /home/hadoop/.jupyter/labconfig/

USER hadoop

RUN cs launch --use-bootstrap almond \
        --scala ${SCALA_VERSION} \
        -- \
        --install \
        --force

ENV PATH="/home/hadoop/.local/bin:${PATH}"
