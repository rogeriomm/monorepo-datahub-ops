# Databricks Free Edition Infrastructure

## Databricks Git Folder

![Databricks Git folder repository contents](attachments/databricks-git-folder-repository-contents.png)

## Git Web Terminal

- Uses [tmux](https://github.com/tmux/tmux/wiki).
- Includes Vim, Git, and the Databricks CLI.
- Runs on an ARM processor.

![Databricks setting to export IPYNB output from repositories](attachments/databricks-repos-ipynb-output-setting.png)

![Databricks web terminal system inspection](attachments/databricks-web-terminal-system-inspection.png)

![Git pull in the Databricks web terminal](attachments/databricks-web-terminal-git-pull.png)

![Databricks CLI clusters list](attachments/databricks-cli-clusters-list.png)

![Terminated Spark driver error](attachments/databricks-terminated-spark-driver-error.png)

```shell
tmux show-options -g prefix
tmux list-keys | grep window
```

- Enable **Allow repos to export IPYNB output**.

![Allow repos to export IPYNB output setting](attachments/databricks-repos-ipynb-output-setting.png)

## Databricks Free Edition Internals

### Serverless Environment Versions

- [Serverless environment versions](https://docs.databricks.com/aws/en/release-notes/serverless/environment-version)
- [Databricks Connect](https://docs.databricks.com/aws/en/dev-tools/databricks-connect/)
- [Spark Connect overview](https://spark.apache.org/docs/latest/spark-connect-overview.html)

![Spark Connect architecture](attachments/spark-connect-architecture.png)

## Running Background Processes

![Background processes are not supported](attachments/databricks-background-processes-not-supported.png)

## Network

![Databricks notebook network and SSH test](attachments/databricks-notebook-network-ssh-test.png)

[Databricks CLI sample notebook](../../../notebooks/jupyter/databricks/free-edition/databricks-cli-hello-world.ipynb)
