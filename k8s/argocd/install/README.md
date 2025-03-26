   * https://github.com/marketplace/actions/argo-cd-action
   * https://argo-cd.readthedocs.io/en/stable/


   * https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd

   * https://medium.com/@kumarkotamahesh/how-to-install-argocd-in-ubuntu-using-k3s-as-light-weighted-kubernetes-99c2f3af3434

```shell
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```