# Mise tasks

```shell
cd on-premises/k8s
```

```shell
mise run k3s:cluster:create
```

```shell
mise run k3s:cluster:start
```

```shell
mise run k3s:cluster:stop
```

```shell
kubectl get nodes
kubectl get pods -A
```

```shell
mise run k3s:cluster:delete
```

# oh my zsh plugins
 - https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/kubectl
 - https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/helm

```shell
alias kgpa
kgpa
```

![[Pasted image 20260929104100.png|1234]]
# K3S
![[Pasted image 20260929101136.png|1215]]


# Install Argo CD
 - Legacy install, don't use: [[on-premises/k8s/argocd/install/README]]

- https://github.com/argoproj/argo-helm/tree/argo-cd-10.9.3

```shell
helm repo add argo https://argoproj.github.io/argo-helm
helm repo list
```


```shell
helm uninstall argo
```



```shell
k3d cluster create argocd \
  --servers 1 \
  --agents 1 \
  -p "8081:80@loadbalancer" \
  -p "8445:443@loadbalancer"
```

- http://localhost:8081
- https://localhost:8445

```shell
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

```shell
helm search repo argo/argo-cd --versions | grep 10.9.3
```

```shell
cd on-premises/k8s/argocd/install
```

```shell
helm upgrade --install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --version 10.9.3 \
  -f values.yaml
```


Argo CD user admin, password:
```shell
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 --decode; echo
```

```shell
argocd admin initial-password -n argocd
```

![[Pasted image 20260929130359.png|1154]]
# Issues
## ArgoCD repo-server fails
Check DNS, WIFI & Ethernet


# Local links
 - http://argocd.localhost:8081/
	 - https://argocd.localhost:8081/

# See also
 - [[Development Containers]]

# Links
 - https://k3d.io/stable/#releases
 - https://ohmyz.sh/
	 - https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/kubectl
	 - https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/helm
	 - https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/mise