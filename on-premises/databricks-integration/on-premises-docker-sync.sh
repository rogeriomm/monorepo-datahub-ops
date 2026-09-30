#!/usr/bin/env zsh

set -o errexit -o nounset -o pipefail

TARGET="pve-vm"

# mTLS certificates server and client

scp ../docker/postgres/certificates/* \
  $TARGET:~/git/monorepo-datahub-ops-private/on-premises/docker/postgres/certificates/


scp ../docker/trino/certificates/* \
  $TARGET:~/git/monorepo-datahub-ops-private/on-premises/docker/trino/certificates/


scp ../docker/rustfs/certificates/* \
  $TARGET:~/git/monorepo-datahub-ops-private/on-premises/docker/rustfs/certificates/
