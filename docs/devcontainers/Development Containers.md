# Development Containers

- [DevPod](https://devpod.sh/)

<img src="attachments/devpod-feature.png" alt="DevPod feature overview" width="200">

## Start a development container
## Using terminal

```shell
devpod up . --ide none
```

<img src="attachments/devpods-sample-1.png" alt="DevPod development container example" width="900">

## Using Visual Studio Code
```shell
devpod up . --ide vscode
```

<img src="attachments/Pasted image 20260729112911.png" alt="DevPod development container example" width="900">

## Traefik reverse proxy

Open the [Traefik dashboard](http://traefik.localhost:8080/dashboard/) to access the administration interface.

<img src="attachments/reverse-proxy-admin-1.png" alt="Traefik administration interface" width="800">

## Jupyter notebooks

See the [local services](#local-services) for the available Jupyter endpoints.

## Zeppelin notebooks

See the [local services](#local-services) for the available Zeppelin endpoint.

## Airflow

Get the administrator password using the repository's
[`docker-compose.yaml`](../../.devcontainer/docker-compose.yaml) file:

```shell
docker compose -f .devcontainer/docker-compose.yaml exec airflow-3.3 \
  cat /opt/airflow/simple_auth_manager_passwords.json.generated
```

## Local S3 object store

Use the AWS CLI to connect directly:

```shell
AWS_ACCESS_KEY_ID=admin AWS_SECRET_ACCESS_KEY=secret \
aws --endpoint-url http://localhost:8333 s3 ls
```

Or connect through Traefik:

```shell
AWS_ACCESS_KEY_ID=admin AWS_SECRET_ACCESS_KEY=secret \
aws --endpoint-url http://seaweedfs-s3.localhost:8080 s3 ls
```

## AWS

### CLI

Install the AWS CLI on the host using [mise](https://mise.jdx.dev/installing-mise.html), then log in with an AWS account.

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

![AWS CLI browser login](<attachments/Pasted image 20260729100251.png>)

![AWS CLI login confirmation](<attachments/Pasted image 20260729095857.png>)

Verify the authenticated identity:

```shell
aws sts get-caller-identity --profile administrator | jq
```

![AWS identity returned by the CLI](<attachments/Pasted image 20260729100657.png>)

List the available S3 buckets:

```shell
aws s3 ls --profile administrator
```

![S3 buckets returned by the CLI](<attachments/Pasted image 20260729100605.png>)

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

![AWS identity returned inside the development container|2147](<attachments/Pasted image 20260729104847.png>)

![[Pasted image 20260729112809.png|1440]]

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
- Zeppelin
  - [Zeppelin 0.12.1](http://zeppelin-0.12.1.localhost:8080)
- Kafka
  - [Kafka UI](http://kafka-ui.localhost:8080)
- S3 object storage
  - [SeaweedFS master](http://seaweedfs-master.localhost:8080)
  - [SeaweedFS filer](http://seaweedfs-filer.localhost:8080)
  - [SeaweedFS S3](http://seaweedfs-s3.localhost:8080)
- Airflow
  - [Airflow 3.3](http://airflow-3-3.localhost:8080/)
  - [Airflow 2.11](http://airflow-2-11.localhost:8080/)

## References

- [VS Code dev container with Zsh, Oh My Zsh, and the Agnoster theme](https://medium.com/@jamiekt/vscode-devcontainer-with-zsh-oh-my-zsh-and-agnoster-theme-8adf884ad9f6)
  - [My data engineering development setup — March 2022](https://medium.com/@jamiekt/my-dev-setup-march-2022-e89d21b19fe6)
- [Development Container JSON schema](https://github.com/devcontainers/spec/blob/main/schemas/devContainer.base.schema.json)
- [Development Container Dockerfile guide](https://containers.dev/guide/dockerfile)
