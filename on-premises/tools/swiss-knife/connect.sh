#!/usr/bin/env bash

# Name of the container
CONTAINER_NAME="tool"

# Optional: fetch the internal container IP (not required for SSH)
CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_NAME)

echo "Container internal IP: $CONTAINER_IP"
echo "Connecting via SSH on localhost:9998 ..."

ssh -p 9998 dev@localhost
