#!/usr/bin/env zsh

# https://hub.docker.com/r/bitnamicharts/argo-cd

# Function to install or upgrade Argo CD to the latest Helm chart version
argocd_install() {
  helm upgrade --install argo-cd oci://registry-1.docker.io/bitnamicharts/argo-cd \
    --namespace argo-cd \
    --create-namespace \
    --values "values.yaml" \
    --values "values_vm.pvel.yaml" \
    --wait \
    --timeout 600s \
    --debug || { echo "❌ Argo CD install/upgrade failed"; return 1; }
}

# Execute function
argocd_install
