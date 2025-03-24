# Passwords
- https://github.com/goharbor/harbor-helm/blob/ac65d7b4d6dd5f42b0e1521be2c488bc1663b1c4/values.yaml#L270
```shell
kubectl -n harbor get secrets harbor-registry-htpasswd -o yaml | yq
```
```yaml
apiVersion: v1
data:
  REGISTRY_HTPASSWD: aGFyYm9yX3JlZ2lzdHJ5X3VzZXI6JDJhJDEwJHZGVWZFc09lRWhoVTguT0tTQ25GaS5LWFhrNXlOMWZsLnhRNmtQZ3U2c0hMM09Rd2N1aUZp
kind: Secret
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: harbor:/Secret:harbor/harbor-registry-htpasswd
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"REGISTRY_HTPASSWD":"aGFyYm9yX3JlZ2lzdHJ5X3VzZXI6JDJhJDEwJHZGVWZFc09lRWhoVTguT0tTQ25GaS5LWFhrNXlOMWZsLnhRNmtQZ3U2c0hMM09Rd2N1aUZp"},"kind":"Secret","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"harbor:/Secret:harbor/harbor-registry-htpasswd"},"labels":{"app":"harbor","app.kubernetes.io/instance":"harbor","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"harbor","app.kubernetes.io/part-of":"harbor","app.kubernetes.io/version":"2.13.0","chart":"harbor","heritage":"Helm","release":"harbor"},"name":"harbor-registry-htpasswd","namespace":"harbor"},"type":"Opaque"}
  creationTimestamp: "2025-06-03T18:31:16Z"
  labels:
    app: harbor
    app.kubernetes.io/instance: harbor
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: harbor
    app.kubernetes.io/part-of: harbor
    app.kubernetes.io/version: 2.13.0
    chart: harbor
    heritage: Helm
    release: harbor
  name: harbor-registry-htpasswd
  namespace: harbor
  resourceVersion: "240342"
  uid: 92f76d24-e0c2-4bbb-a9ca-e9c938a78b0f
type: Opaque
```


# Links 
- https://goharbor.io/
   - https://goharbor.io/docs/2.4.0/install-config/harbor-ha-helm/