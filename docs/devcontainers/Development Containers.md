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
- https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html
```shell
aws configure list-profiles
```

```shell
unset AWS_CA_BUNDLE 
unset REQUESTS_CA_BUNDLE 
unset SSL_CERT_FILE
```

 - Login user "administrator"
```shell
aws login --profile administrator
```

- whoami
```shell
aws sts get-caller-identity --profile administrator
```

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
