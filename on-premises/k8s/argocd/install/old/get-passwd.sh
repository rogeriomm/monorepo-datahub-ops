kubectl get secret argocd-secret -n argo-cd -o jsonpath="{.data.clearPassword}" | base64 --decode

