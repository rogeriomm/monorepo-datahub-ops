FROM spark:3.5.7 as spark

USER root

RUN set -ex && \
    cd /usr/local && \
    wget --remote-encoding=utf-8 -qO- https://micromamba.snakepit.net/api/micromamba/linux-64/latest | tar -xvj bin/micromamba

COPY env_python_3_with_R.yml /env_python_3_with_R.yml

RUN set -ex && \
    micromamba create -y -p /opt/conda -f /env_python_3_with_R.yml && \
    micromamba clean -ay

RUN set -ex && \
    DEBIAN_FRONTEND=noninteractive apt-get purge -y python3.10 && \
    DEBIAN_FRONTEND=noninteractive apt-get autoremove -y

ENV PATH=/opt/conda/bin:$PATH

#USER spark
