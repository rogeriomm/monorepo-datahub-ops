# Recreate the Airflow connections

```shell
docker compose up -d --force-recreate airflow-3.3 airflow-2.11
```

 - Script that creates the Airflow connections: [configure-connections.sh](../../on-premises/docker/airflow/configure-connections.sh)