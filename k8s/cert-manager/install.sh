helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.15.1 \
  --set crds.enabled=true \
  --set webhook.timeoutSeconds=4 \
  --set replicaCount=2 \
  --set podDisruptionBudget.enabled=true \
  --set podDisruptionBudget.minAvailable=1

