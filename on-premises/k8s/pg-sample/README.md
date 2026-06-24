 - Password
```shell
kubectl get secret cluster-example-app -n pg-example -o jsonpath='{.data.password}' | base64 -d
```

```shell
psql -h 192.168.15.161 -p 5432 -U app -d app
```