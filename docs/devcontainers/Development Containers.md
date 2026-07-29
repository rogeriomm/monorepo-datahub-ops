# Development Containers
- https://devpod.sh/
    - <img src="attachments/devpod-feature.png" alt="drawing" width="200"/>


```shell
devpod up . --ide none
```

<img src="attachments/devpods-sample-1.png" alt="drawing" width="800"/>

# Traefik Reverse proxy
- http://traefik.localhost:8080/dashboard/ Traefik admin interface 
<img src="attachments/reverse-proxy-admin-1.png" alt="drawing" width="800"/>

# Jupyter Notebooks

# Zeppelin Notebooks

# Airflow
- Get administrator password
```shell
docker compose -f .devcontainer/docker-compose.yaml exec airflow-3.3 \
  cat /opt/airflow/simple_auth_manager_passwords.json.generated
```



## Local S3 object store
- AWS CLI
```shell
AWS_ACCESS_KEY_ID=admin AWS_SECRET_ACCESS_KEY=secret \
aws --endpoint-url http://localhost:8333 s3 ls
```

 - Via Traefik
```shell
AWS_ACCESS_KEY_ID=admin AWS_SECRET_ACCESS_KEY=secret \
aws --endpoint-url http://seaweedfs-s3.localhost:8080 s3 ls
```

# AWS
## CLI
Install the AWS CLI on the host using [mise](https://mise.jdx.dev/installing-mise.html), then log in with an AWS account.
```
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

Log in as the `administrator` user on the host
```shell
aws login --profile administrator
```

![[Pasted image 20260729100251.png|1085]]

![[Pasted image 20260729095857.png|1086]]

Verify the authenticated identity:
```shell
aws sts get-caller-identity --profile administrator | jq
```

![[Pasted image 20260729100657.png|1086]]

```shell
aws s3 ls --profile administrator
```

![[Pasted image 20260729100605.png|1095]]

Start the dev container:
```shell
devpod down .
devpod up . --ide none
ssh monorepo-datahub-ops-private.devpod
```

Inside the dev container, unset the AWS environment variables that override the selected profile:
```shell
unset AWS_ACCESS_KEY_ID AWS_CONFIG_FILE AWS_REGION AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
```

Then verify the authenticated AWS identity:

```shell
aws sts get-caller-identity --profile administrator | jq
```


![[Pasted image 20260729104847.png|1089]]

# Databricks
## CLI
[📓 databricks-cli-hello-world.ipynb](http://jupyter-spark-4-1.localhost:8080/notebooks/databricks/free-edition/databricks-cli-hello-world.ipynb) [[databricks-cli-hello-world.ipynb]]


# Local links
- Reverse proxy
	- http://traefik.localhost:8080/dashboard/ Traefik admin interface
	- Jupyter
		- http://jupyter-spark-3-5.localhost:8080/lab
		- http://jupyter-spark-4.1.localhost:8080/lab
	- AWS GLUE
		- http://jupyter-glue-5.localhost:8080/lab
	- Zeppelin
		- http://zeppelin-0.12.1.localhost:8080
	- Kafka
		- http://kafka-ui.localhost:8080
	- S3 object storage
		- http://seaweedfs-master.localhost:8080
		- http://seaweedfs-filer.localhost:8080
		- http://seaweedfs-s3.localhost:8080		
	- Airflow		
		- http://airflow-3-3.localhost:8080/
		- http://airflow-2-11.localhost:8080/

# Links
 - [VSCode devcontainer with zsh, oh-my-zsh and agnoster theme](https://medium.com/@jamiekt/vscode-devcontainer-with-zsh-oh-my-zsh-and-agnoster-theme-8adf884ad9f6)
    - [My data engineering dev setup — March 2022](https://medium.com/@jamiekt/my-dev-setup-march-2022-e89d21b19fe6)
- [Devcontainer JSON schema](https://github.com/devcontainers/spec/blob/main/schemas/devContainer.base.schema.json)
