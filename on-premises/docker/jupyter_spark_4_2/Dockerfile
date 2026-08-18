ARG BASE_IMAGE=local/jupyter-pyspark-base:4.2.0
FROM ${BASE_IMAGE}

ARG SCALA_VERSION=2.13.17

USER root

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        curl gzip tree figlet toilet zsh \
        build-essential \
        libpq-dev \
        python3-dev \
        apt-file \
        netcat-openbsd  nmap net-tools inetutils-ping bsdextrautils \
        postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

RUN curl --fail --location \
        https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux.gz \
        --output /tmp/cs.gz \
    && gzip --decompress /tmp/cs.gz \
    && install -m 0755 /tmp/cs /usr/local/bin/cs \
    && rm -f /tmp/cs

RUN pip install --no-cache-dir \
    pandas parquet-tools kagglehub contexttimer rich findspark \
    humanize ipython-autotime sparkmonitor itables

RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/jovyan \
  && chmod 0440 /etc/sudoers.d/jovyan

# Copy external .zshrc from project directory
COPY fs/home/jovyan/ /home/jovyan/

# Fix ownership
RUN chown -R jovyan /home/jovyan

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

# Install mise: https://mise.jdx.dev/getting-started.html
RUN --mount=type=secret,id=GITHUB_TOKEN,env=GITHUB_TOKEN \
    curl https://mise.run | sh

RUN echo 'eval "$($HOME/.local/bin/mise activate bash)"' >> "$HOME/.bashrc"

RUN --mount=type=secret,id=GITHUB_TOKEN,env=GITHUB_TOKEN \
    bash -lc 'eval "$($HOME/.local/bin/mise activate bash)" \
    && mise install \
    && mise install java@jetbrains-11.0.16-b2043.64 java@17'

USER root

COPY jupyterlab-overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json

ENV SPARK_HOME=/usr/local/spark
# Notebook kernels do not source interactive shell startup files. Keep mise's
# shims on the image-level PATH so kernels can resolve mise-managed commands.
ENV PATH="/home/jovyan/.local/share/mise/shims:/home/jovyan/.local/bin:${SPARK_HOME}/bin:${PATH}"

COPY fs/home/jovyan/.zshrc /home/jovyan/.zshrc
# Fix ownership
RUN chown -R jovyan /home/jovyan/.zshrc

USER ${NB_UID}

WORKDIR "${HOME}/work"
