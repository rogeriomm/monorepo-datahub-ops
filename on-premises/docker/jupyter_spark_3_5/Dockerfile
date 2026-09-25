ARG BASE_IMAGE=local/jupyter-pyspark-base:3.5.9
FROM ${BASE_IMAGE}

ARG SCALA_VERSION=2.12.20
ARG COURSIER_VERSION=2.1.25-M26

USER root

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        curl \
        gzip \
        build-essential \
        libpq-dev \
        python3-dev \
        apt-file zsh \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    case "$(dpkg --print-architecture)" in \
      amd64) coursier_arch=x86_64; coursier_sha256=017812b4da91a72fadd3cb0fb97caae4a16cb947a7bd6be2b46e5aa984458cbf ;; \
      arm64) coursier_arch=aarch64; coursier_sha256=68288bcd47a81f3a3bcf0392572d40ec0981172bba9055a8b662413691358be9 ;; \
      *) echo "Unsupported Coursier architecture: $(dpkg --print-architecture)" >&2; exit 1 ;; \
    esac; \
    curl --fail --silent --show-error --location \
      "https://github.com/coursier/coursier/releases/download/v${COURSIER_VERSION}/cs-${coursier_arch}-pc-linux.gz" \
      --output /tmp/cs.gz; \
    echo "${coursier_sha256} */tmp/cs.gz" | sha256sum --check --strict; \
    gzip --decompress /tmp/cs.gz; \
    install -m 0755 /tmp/cs /usr/local/bin/cs; \
    rm -f /tmp/cs; \
    cs version

RUN pip install --no-cache-dir \
    pandas parquet-tools kagglehub contexttimer rich findspark \
    humanize ipython-autotime

RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/jovyan \
  && chmod 0440 /etc/sudoers.d/jovyan

# Copy the shell and mise configuration into the Jupyter user's home.
COPY fs/home/jovyan/ /home/jovyan/

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

# Spark 3.5 runs on Java 17. Keep Java 11 available for older project tools,
# without activating either mise-managed JVM over the image's Java 17.
RUN --mount=type=secret,id=GITHUB_TOKEN,env=GITHUB_TOKEN \
    bash -lc 'eval "$($HOME/.local/bin/mise activate bash)" \
    && mise install \
    && mise install java@jetbrains-11.0.16-b2043.64 java@17'

USER root

COPY jupyterlab-overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json

ENV SPARK_HOME=/usr/local/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"

COPY fs/home/jovyan/.zshrc /home/jovyan/.zshrc
RUN chown -R jovyan /home/jovyan/.zshrc

USER ${NB_UID}

WORKDIR "${HOME}/work"
