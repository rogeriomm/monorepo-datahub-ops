#!/usr/bin/env bash

docker-ip() {
  local IMAGE_NAME="$1"
  local id name ip

  [[ -z "$IMAGE_NAME" ]] && return 1

  id=$(docker ps -q --filter "ancestor=${IMAGE_NAME}" | head -n 1) || return 1
  name=$(docker ps --filter "id=$id" --format "{{.Names}}")
  ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$id")

  DOCKER_CONTAINER_NAME="$name"
  DOCKER_CONTAINER_IP="$ip"
}


docker-ip tool

print "Name: $DOCKER_CONTAINER_NAME"
print "IP:   $DOCKER_CONTAINER_IP"

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      dev@"${DOCKER_CONTAINER_IP}"
