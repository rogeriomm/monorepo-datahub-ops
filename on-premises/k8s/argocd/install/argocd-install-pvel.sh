helm upgrade --install argocd argo/argo-cd \
  --namespace argo-cd \
  --create-namespace \
  --version 10.9.3 \
  -f values-pvel.yaml