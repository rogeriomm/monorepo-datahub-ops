   * https://medium.com/@randeniyamalitha08/enabling-argocd-metrics-and-monitoring-using-kube-prometheus-stack-ebece18c41d8

# Grafana
```shell
kubectl get secret -n prometheus prometheus-grafana -o jsonpath="{.data.admin-user}" | base64 -d
```

```shell
kubectl get secret -n prometheus prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 -d
```
# Add servers with metrics

```shell
kubectl port-forward -n prometheus svc/prometheus-kube-prometheus-prometheus 9090:9090
```
```shell
curl -s http://localhost:9090/api/v1/status/config | jq -r '.data.yaml' | yq
```

 - Go to Grafana Explorer
 - In the query field, type:
```plain text
 up{job="external-app"}
 ```