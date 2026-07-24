- Databricks Git folder

![[databricks-git-folder-repository-contents.png]]
# GIT Web Terminal

 
	 - Uses [tmux](https://github.com/tmux/tmux/wiki)
	 - vim, git, Databricks CLI
	 - ARM processor
	
![[databricks-repos-ipynb-output-setting.png]]
![[databricks-web-terminal-system-inspection.png]]
![[databricks-web-terminal-git-pull.png]]
![[databricks-cli-clusters-list.png]]
![[databricks-terminated-spark-driver-error.png]]

 ```shell
 tmux show-options -g prefix
 tmux list-keys | grep window
 ```

 - Enable "Allow repos to export IPYNB output"
![[databricks-repos-ipynb-output-setting.png]]



# Databricks free-edition internals
## Serverless environment versions
- https://docs.databricks.com/aws/en/release-notes/serverless/environment-version
	- https://docs.databricks.com/aws/en/dev-tools/databricks-connect/
	- https://spark.apache.org/docs/latest/spark-connect-overview.html

![[spark-connect-architecture.png]]
# Running background process

![[databricks-background-processes-not-supported.png]]

# Network
![[databricks-notebook-network-ssh-test.png]]![[databricks-cli-hello-world.ipynb]]
[[databricks-cli-hello-world.ipynb|Databricks CLI sample notebook]]
