```shell
umask 077

argocd admin export \
  --namespace argo-cd \
  --application-namespaces argo-cd \
  --applicationset-namespaces argo-cd \
  --out argocd-export.yaml
```

```shell
umask 077

helm get values argo-cd -n argo-cd --all \
  > argo-cd-bitnami-values.yaml

helm get manifest argo-cd -n argo-cd \
  > argo-cd-bitnami-manifest.yaml

kubectl get ingress argo-cd-server -n argo-cd -o yaml \
  > argo-cd-ingress.yaml

kubectl get secret argo-cd.ing.vm.pvel.worldl.xpt-tls -n argo-cd -o yaml \
  > argo-cd-ingress-tls.yaml
```
  

```shell
helm uninstall argo-cd \
  --namespace argo-cd \
  --wait \
  --timeout 10m
```

```shell
argocd admin import
```

 - https://argo-cd.readthedocs.io/en/stable/operator-manual/installation
