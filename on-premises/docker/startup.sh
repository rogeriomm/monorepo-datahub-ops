#!/bin/sh

set -eu

echo "Running Docker Compose startup tasks"

HOME="/home/local"

id

touch $HOME/.tmux.conf
touch $HOME/.config
touch $HOME/.databrickscfg

# /var/run/docker.sock
# /opt/jetbrains/agent.jar

mkdir -p $HOME/.m2 \
       $HOME/.local/share/mise \
       $HOME/.tmux \
       $HOME/.aws \
       $HOME/.aws/login/cache \
       $HOME/.databricks

echo "Docker Compose startup tasks completed"
