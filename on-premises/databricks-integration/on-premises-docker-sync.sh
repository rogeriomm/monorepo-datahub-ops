#!/usr/bin/env zsh

TARGET="pve-vm"

# mTLS certificates server and client
scp ../docker/trino/certificates/* \
  $TARGET:~/git/monorepo-datahub-ops-private/on-premises/docker/trino/certificates/