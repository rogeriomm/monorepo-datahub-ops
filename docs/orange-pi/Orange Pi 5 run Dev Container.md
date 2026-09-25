```shell
cd ~/git/monorepo-datahub-ops-private/on-premises/docker
```


```shell
docker compose build pyspark-base-3.5
docker compose build jupyter-spark-3.5

docker compose build pyspark-base-4.1
docker compose build jupyter-spark-4.1

docker compose build pyspark-base-4.2
docker compose build jupyter-spark-4.2
```


```shell
docker compose build airflow-3.3
docker compose build airflow-2.11
docker compose build superset
```

```shell
docker compose build flink-jobmanager 
docker compose build flink-taskmanager
```

```shell
docker compose build zeppelin-0.12.1
```


```shell
docker compose build seaweedfs
```

```shell
docker compose build hive-metastore
```

```shell
docker compose build  obsidian-mcp-postgres
```

