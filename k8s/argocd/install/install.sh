#!/usr/bin/env zsh

argocd_install() {
  local namespace="argocd"
  local release="argocd"
  local repo_name="argocd"
  local repo_url="https://argoproj.github.io/argo-helm"

  # Extract short hostname (e.g., from "vm.pvel.worldl.xpt" -> "vm.pvel")
  local fqdn=$(hostname)
  local shortname="${fqdn%.worldl.xpt}"
  local values_file="values_${shortname}.yaml"

  echo "🔍 Hostname: $fqdn"
  echo "📄 Using values file: $values_file"

  if [[ ! -f "$values_file" ]]; then
    echo "❌ Values file [$values_file] not found. Aborting."
    return 1
  fi

  echo "🔍 Checking if Argo CD is already installed..."
  if ! helm status "$release" -n "$namespace" >/dev/null 2>&1; then
    echo "📦 Installing Argo CD..."

    echo "➕ Adding Helm repo [$repo_name]..."
    helm repo add "$repo_name" "$repo_url" >/dev/null || {
      echo "❌ Failed to add Helm repo"; return 1
    }

    echo "🔄 Updating Helm repos..."
    helm repo update >/dev/null || {
      echo "❌ Failed to update Helm repos"; return 1
    }

    echo "🚀 Installing Helm chart [$release] in namespace [$namespace]..."
    helm install "$release" "$repo_name/argo-cd" \
      --namespace "$namespace" \
      --create-namespace \
      --values "$values_file" \
      --wait \
      --timeout 600s \
      --debug || {
        echo "❌ Argo CD installation failed"; return 1
      }

    echo "✅ Argo CD installed successfully!"
  else
    echo "✅ Argo CD is already installed in namespace [$namespace]. Skipping installation."
  fi
}

argocd_install
