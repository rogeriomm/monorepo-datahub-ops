# Development Containers

## Table of contents

- [Start a development container](#start-a-development-container)
  - [Using terminal](#using-terminal)
  - [Using Visual Studio Code](#using-visual-studio-code)
- [Traefik reverse proxy](#traefik-reverse-proxy)
- [Jupyter notebooks](#jupyter-notebooks)
- [AWS CLI](#aws-cli)
- [Zeppelin notebooks](#zeppelin-notebooks)
- [Airflow](#airflow)
- [Local S3 object store](#local-s3-object-store)
- [PostgreSQL](#postgresql)
  - [Debugging](#debugging)
  - [Cleaning the database](#cleaning-the-database)
  - [Connect from the host](#connect-from-the-host)
  - [Connect from another container](#connect-from-another-container)
  - [Connect from the PostgreSQL container](#connect-from-the-postgresql-container)
  - [pgAdmin 4](#pgadmin-4)
- [Kafka](#kafka)
- [SSH tunnel](#ssh-tunnel)
- [AWS](#aws)
  - [CLI](#cli)
- [Databricks](#databricks)
  - [CLI](#cli-1)
- [Local services](#local-services)
- [References](#references)

## Start a development container

- [DevPod](https://devpod.sh/)

![DevPod feature overview](attachments/devpod-feature.png)

### Using terminal

```shell
devpod up . --ide none
```

![DevPod development container example](attachments/devpods-sample-1.png)

### Using Visual Studio Code

```shell
devpod up . --ide vscode
```

![DevPod development container in Visual Studio Code](attachments/Pasted%20image%2020260729112911.png)

## Traefik reverse proxy

Open the [Traefik dashboard](http://traefik.localhost:8080/dashboard/) to access the administration interface.

![Traefik administration interface](attachments/reverse-proxy-admin-1.png)

## Jupyter notebooks

See the [local services](#local-services) for the available Jupyter endpoints.

## AWS CLI

- [AWS CLI hello world notebook](../../notebooks/jupyter/aws/aws-cli-hello-world.ipynb)

## Zeppelin notebooks

## Airflow

Get the administrator password using the repository's
[`docker-compose.yaml`](../../.devcontainer/docker-compose.yaml) file:

```shell
docker compose -f .devcontainer/docker-compose.yaml exec airflow-3.3 \
  cat /opt/airflow/simple_auth_manager_passwords.json.generated
```

## Local S3 object store

The direct SeaweedFS S3 endpoint requires TLS. Its development CA certificate
is generated at `.devcontainer/seaweedfs/certificates/ca.crt` when the service
first starts.

Use the AWS CLI to connect directly:
```shell
export AWS_ACCESS_KEY_ID=admin AWS_SECRET_ACCESS_KEY=secret 
export AWS_CA_BUNDLE=.devcontainer/seaweedfs/certificates/ca.crt
export AWS_REGION=us-east-1
```

 - Create a bucket
```shell
aws --endpoint-url https://localhost:8333 \
  s3 mb s3://my-bucket
```

 - Remove a bucket
 ```shell
aws --endpoint-url https://localhost:8333 \
  s3 rm s3://my-bucket
 ```
 - List buckets
```shell
aws --endpoint-url https://localhost:8333 s3 ls
```


Or connect through Traefik:

```shell
aws --endpoint-url http://seaweedfs-s3.localhost:8080 s3 ls
```

![[Pasted image 20260805164131.png|1219]]

[[s3-hello-world.ipynb]]

### Cleaning the S3 object store

```shell
docker volume rm devcontainer_seaweedfs-data
```

## PostgreSQL

PostgreSQL requires TLS for all TCP connections. Its public certificate is
available at `.devcontainer/postgres/certificates/server.crt` after the
container starts. The private key remains inside the PostgreSQL data volume.

### Debugging

```shell
cd .devcontainer
```

```shell
docker compose logs postgres -f
```

Example using Databricks Free Edition and on-premises public endpoint:

![Databricks Free Edition connection using an on-premises public endpoint](attachments/Pasted%20image%2020260805104218.png)

![Databricks Free Edition connection details](attachments/Pasted%20image%2020260805104318.png)

### Cleaning the database

```shell
docker volume rm devcontainer_postgres-data
```

### Connect from the host

Use the `POSTGRES_PORT` value configured for Docker Compose, or port `5432` by
default:

```shell
export PGPORT="${POSTGRES_PORT:-5432}"
export PGSSLMODE=verify-full \
export PGSSLROOTCERT=.devcontainer/postgres/certificates/server.crt \
export PGPASSWORD='postgres'
```

```shell
psql \
  --host=localhost \
  --port=$PGPORT \
  --username=postgres \
  --dbname=postgres
```

![PostgreSQL host connection](attachments/Pasted%20image%2020260805103317.png)

### Connect from another container

For example, connect from `jupyter-spark-4.1` using the Compose service name:

```shell
PGSSLMODE=require \
PGPASSWORD='postgres' \
psql \
  --host=postgres \
  --username=postgres \
  --dbname=postgres
```

### Connect from the PostgreSQL container

```shell
docker compose -f .devcontainer/docker-compose.yaml exec postgres /bin/bash
```

Then switch to the `postgres` user and connect:

```shell
su - postgres
PGSSLMODE=require \
PGPASSWORD='postgres' \
psql \
  --host=localhost \
  --username=postgres \
  --dbname=postgres
```

- [PostgreSQL hello world notebook](../../notebooks/jupyter/postgres/postgres-hello-world.ipynb)

### pgAdmin 4

![PostgreSQL connection configured in pgAdmin 4](attachments/Pasted%20image%2020260804162938.png)

## Kafka

Kafka requires TLS on its internal, host-facing, and KRaft controller
listeners. A development CA and broker certificate are generated on the first
startup under `.devcontainer/kafka-4/certificates/`; the private keys and
stores in that directory are ignored by Git.

The host listener is available at `localhost:9092`. Verify its certificate
with:

```shell
openssl s_client \
  -connect localhost:9092 \
  -servername localhost \
  -CAfile .devcontainer/kafka-4/certificates/ca.crt \
  -verify_return_error </dev/null
```

The `jupyter-spark-4.1` image includes a TLS-enabled [`kafkactl`](https://github.com/deviceinsight/kafkactl) context for
the internal `kafka-4-backend:29092` listener. Kafka UI uses the same trusted CA and is
available through the [local services](#local-services) section.

```shell
docker compose -f .devcontainer/docker-compose.yaml \
  exec jupyter-spark-4.1 \
  bash -lc 'eval "$($HOME/.local/bin/mise activate bash)" && kafkactl get topics'
```

## SSH tunnel

> [!NOTE]
> An SSH tunnel is not a full VPN, but it can be used in a similar way to
> securely access services on a private network from Databricks Free Edition
> or other Databricks environments.
>
> In [Databricks Free Edition](https://www.databricks.com/learn/free-edition),
> an [SSH tunnel](https://en.wikipedia.org/wiki/Tunneling_protocol) is the only
> available option for this type of private-network access.

```ssh
ssh -p 9023 \
  -i ~/.ssh/id_ed25519_databricks_free \
  -o BatchMode=yes \
  -o StrictHostKeyChecking=accept-new \
  -o ControlMaster=auto \
  -o ControlPath=/tmp/ssh-databricks \
  -o ControlPersist=10m \
  -o UserKnownHostsFile=/tmp/known_hosts \
  tunnel@localhost
```

## AWS

### CLI

Install the AWS CLI on the host using
[mise](https://mise.jdx.dev/installing-mise.html), then log in with an AWS
account.

```shell
mise install aws-cli
```

Unset custom certificate-related environment variables, if necessary:

```shell
unset AWS_CA_BUNDLE
unset REQUESTS_CA_BUNDLE
unset SSL_CERT_FILE
```

List the configured AWS CLI profiles:

```shell
aws configure list-profiles
```

Log in as the `administrator` user on the host:

```shell
aws login --profile administrator
```

![AWS CLI browser login](attachments/Pasted%20image%2020260729100251.png)

![AWS CLI login confirmation](attachments/Pasted%20image%2020260729095857.png)

Verify the authenticated identity:

```shell
aws sts get-caller-identity --profile administrator | jq
```

![AWS identity returned by the CLI](attachments/Pasted%20image%2020260729100657.png)

List the available S3 buckets:

```shell
aws s3 ls --profile administrator
```

![S3 buckets returned by the CLI](attachments/Pasted%20image%2020260729100605.png)

Start the development container:

```shell
devpod down .
devpod up . --ide none
ssh monorepo-datahub-ops-private.devpod
```

Inside the development container, unset the AWS environment variables that override the selected profile:

```shell
unset AWS_ACCESS_KEY_ID AWS_CONFIG_FILE AWS_REGION AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_CA_BUNDLE
```

Then verify the authenticated AWS identity:

```shell
aws sts get-caller-identity --profile administrator | jq
```

![AWS identity returned inside the development container](attachments/Pasted%20image%2020260729104847.png)

Using Visual Studio Code:

![AWS identity verification in the development container](attachments/Pasted%20image%2020260729112809.png)

## Databricks

### CLI

- [Databricks CLI hello world notebook](../../notebooks/jupyter/databricks/free-edition/databricks-cli-hello-world.ipynb)
- [Open the notebook in the local Jupyter service](http://jupyter-spark-4-1.localhost:8080/notebooks/databricks/free-edition/databricks-cli-hello-world.ipynb)

## Local services

- Reverse proxy
  - [Traefik administration interface](http://traefik.localhost:8080/dashboard/)
- Jupyter
  - [Spark 3.5](http://jupyter-spark-3-5.localhost:8080/lab)
  - [Spark 4.1](http://jupyter-spark-4.1.localhost:8080/lab)
- AWS Glue
  - [JupyterLab](http://jupyter-glue-5.localhost:8080/lab)
- Kafka
  - [Kafka UI](http://kafka-ui.localhost:8080)
- Zeppelin
  - [Zeppelin 0.12.1](http://zeppelin-0.12.1.localhost:8080)
- S3 object storage
  - [SeaweedFS master](http://seaweedfs-master.localhost:8080)
  - [SeaweedFS filer](http://seaweedfs-filer.localhost:8080)
  - [SeaweedFS S3](http://seaweedfs-s3.localhost:8080)
- Airflow
  - [Airflow 3.3](http://airflow-3-3.localhost:8080/)
  - [Airflow 2.11](http://airflow-2-11.localhost:8080/)
- Trino
  - [Trino dashboard](http://trino.localhost:8080/ui)

## References

- [Video: My Entire Neovim + Tmux + Workflow (2026 Update)](https://youtu.be/fjoGZ90bOzw?t=2947)
  - [Video: Stateless Workstation](https://youtu.be/S6T5M4jLqR8?t=1410)
- [VS Code dev container with Zsh, Oh My Zsh, and the Agnoster theme](https://medium.com/@jamiekt/vscode-devcontainer-with-zsh-oh-my-zsh-and-agnoster-theme-8adf884ad9f6)
  - [My data engineering development setup — March 2022](https://medium.com/@jamiekt/my-dev-setup-march-2022-e89d21b19fe6)
- [Development Container JSON schema](https://github.com/devcontainers/spec/blob/main/schemas/devContainer.base.schema.json)
- [Development Container Dockerfile guide](https://containers.dev/guide/dockerfile)
- [Coder](https://github.com/coder/coder)
