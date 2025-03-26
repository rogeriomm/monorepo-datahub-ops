argocd_install()
{
  if ! helm status argocd -n argocd 2> /dev/null > /dev/null; then
    helm repo add argocd https://argoproj.github.io/argo-helm
    helm repo update argocd
    helm install --namespace argocd --create-namespace argocd  \
        argocd/argo-cd --values ./values.yaml \
        --wait --timeout 600s --debug
  fi
}

argocd_install
