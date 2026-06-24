#!/usr/bin/env bash

#export UID="$(id -u)"
export UID 
export GID="$(id -g)"
#export UID="1002"
#export GID="1002"

export GITHUB_TOKEN=$(gh auth token)
echo "Github token: $GITHUB_TOKEN"

#docker compose build
docker compose build --progress=plain $1
#docker compose build --progress=plain --no-cache

