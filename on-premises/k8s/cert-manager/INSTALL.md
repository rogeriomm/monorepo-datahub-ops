
# Install
```shell
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

```shell
kubectl -n cert-manager apply -f spnw-root-ca.yaml
```

```shell
kubectl get secret spnw-root-ca-secret -n cert-manager -o jsonpath='{.data.tls\.crt}' |  base64 --decode | openssl x509 -noout -text
```

```shell
kubectl get secret spnw-intermediate-ca1-secret -n cert-manager -o jsonpath='{.data.tls\.crt}' |  base64 --decode | openssl x509 -noout -text
```

## Test certificate
```shell
kubectl apply -f test-cert.yaml
```
```shell
kubectl -n cert-test get certificates
```
```shell
kubectl -n cert-test get certificates test-server -o yaml | yq
```


# Links 
   - https://raymii.org/s/tutorials/Self_signed_Root_CA_in_Kubernetes_with_k3s_cert-manager_and_traefik.html
   - https://github.com/cert-manager/cert-manager