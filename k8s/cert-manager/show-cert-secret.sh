kubectl describe -n cert-manager secret/spnw-root-ca-secret
echo "====================================="
kubectl get secret spnw-root-ca-secret -n cert-manager -o jsonpath='
{.data.tls\.crt}' |  base64 --decode | openssl x509 -noout -text

