ARG BASE_IMAGE=local/jupyter-pyspark-base:4.1.3
FROM ${BASE_IMAGE}

ARG SCALA_VERSION=2.13.17
ARG COURSIER_VERSION=2.1.25-M26
ARG DOCKER_COMPOSE_VERSION=5.5.1

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
        docker.io \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    case "$(dpkg --print-architecture)" in \
      amd64) compose_arch=x86_64; compose_sha256=db1889184726840f75c4f9c001048430d4f25b3be3cb084d3ddd762bc0aed576 ;; \
      arm64) compose_arch=aarch64; compose_sha256=732e3a84c1a0f67256ce80bc2598a24546b10ca05f9faa97efceb1171ece2ef7 ;; \
      *) echo "Unsupported Docker Compose architecture: $(dpkg --print-architecture)" >&2; exit 1 ;; \
    esac; \
    compose_plugin=/usr/local/lib/docker/cli-plugins/docker-compose; \
    mkdir -p "$(dirname "${compose_plugin}")"; \
    curl --fail --silent --show-error --location \
      "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-linux-${compose_arch}" \
      --output "${compose_plugin}"; \
    echo "${compose_sha256} *${compose_plugin}" | sha256sum --check --strict; \
    chmod +x "${compose_plugin}"; \
    docker compose version

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
    humanize ipython-autotime sparkmonitor itables aws-sdk-python trino \
    jupyter-mcp-server jupyter-mcp-tools

# Streamable HTTP notifications have no JSON-RPC response body. A 202 status
# tells MCP clients that the notification was accepted; jupyter-mcp-server
# currently returns an empty 200 SSE response, which Codex rejects.
RUN sed --in-place \
        '/if request_id is None:/,/^[[:space:]]*return$/ s/self\.set_status(200)/self.set_status(202)/' \
        /opt/conda/lib/python*/site-packages/jupyter_mcp_server/jupyter_extension/handlers.py \
    && grep --quiet \
        'self.set_status(202)' \
        /opt/conda/lib/python*/site-packages/jupyter_mcp_server/jupyter_extension/handlers.py

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
