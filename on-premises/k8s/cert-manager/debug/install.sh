helm upgrade --install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.19.0 \
  --set crds.enabled=true \
  --set webhook.timeoutSeconds=4 \
  --set replicaCount=1 \
  --set podDisruptionBudget.enabled=true \
  --set podDisruptionBudget.minAvailable=1

