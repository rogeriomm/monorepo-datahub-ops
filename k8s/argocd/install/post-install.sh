kubectl config set-context --current --namespace argo-cd
argocd login world1l.worldl.xpt --core
argocd repo add https://charts.bitnami.com/bitnami --type helm --name bitnami
