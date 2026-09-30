# Local Kubernetes with K3D

This guide creates a local [K3D](https://k3d.io/) cluster and installs
[Argo CD](https://argo-cd.readthedocs.io/) with Helm. Run the commands from the
repository root unless a section specifies another directory.

## Prerequisites

- Docker
- [Mise](https://mise.jdx.dev/)
- `kubectl`
- `k3d`

The project configuration also provides Helm, K9s, the Argo CD CLI, and Gum.
Install the configured tools before creating the cluster:

```shell
cd on-premises/k8s
mise install
```

## Manage the cluster

The Mise tasks create and manage a cluster named `argocd` with one server and
one agent. The load balancer exposes HTTP on port `8081` and HTTPS on port
`8445`.

### Create the cluster

```shell
cd on-premises/k8s
mise run k3d:cluster:create
```

### Inspect the cluster

```shell
kubectl get nodes
kubectl get pods --all-namespaces
```

### Stop and start the cluster

```shell
mise run k3d:cluster:stop
mise run k3d:cluster:start
```

### Delete the cluster

```shell
mise run k3d:cluster:delete
```

The delete task asks for confirmation and selects **No** by default.

## Install Argo CD

Add and update the Argo Helm repository:

```shell
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm show chart argo/argo-cd --version 10.9.3
```

Run the project installer:

```shell
cd on-premises/k8s/argocd/install
./argocd-install.sh
```

The installer deploys chart version `10.9.3` to the `argocd` namespace using
the local values file. Wait for the workloads to become ready:

```shell
kubectl -n argocd get pods
kubectl -n argocd rollout status deployment/argocd-server
kubectl -n argocd rollout status deployment/argocd-repo-server
```

Open [Argo CD](http://argocd.localhost:8081/) after the server and ingress are
ready.

## Sign in to Argo CD

The initial username is `admin`. Retrieve the generated password with the Argo
CD CLI:

```shell
argocd admin initial-password --namespace argo-cd
```

Alternatively, read it directly from the Kubernetes secret:

```shell
kubectl -n argo-cd get secret argocd-initial-admin-secret \
  --output jsonpath='{.data.password}' | base64 --decode
echo
```

Change the generated password after the first login:

```shell
argocd account update-password
```

## Troubleshoot the repo server

Check the repo-server status, events, and previous container logs:

```shell
kubectl -n argo-cd get pods
kubectl -n argo-cd describe pods \
  --selector app.kubernetes.io/name=argocd-repo-server
kubectl -n argo-cd logs deployment/argocd-repo-server \
  --container repo-server \
  --previous
```

If `/healthz` succeeds but the `/healthz?full=true` liveness probe times out,
inspect CoreDNS and the DNS servers inherited by the K3D nodes. Switching
between Wi-Fi and Ethernet can leave an unreachable resolver configured for
the cluster.

```shell
kubectl -n kube-system logs deployment/coredns
docker exec k3d-argocd-server-0 cat /etc/resolv.conf
docker exec k3d-argocd-agent-0 cat /etc/resolv.conf
```

## Optional shell helpers

Oh My Zsh provides plugins for the command-line tools used in this guide:

- [kubectl plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/kubectl)
- [Helm plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/helm)
- [Mise plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/mise)

For example, the kubectl plugin provides `kgpa` as an alias for listing pods in
all namespaces:

```shell
kgpa
```

## Project files

- [K3D Mise tasks](../../on-premises/k8s/mise.toml)
- [Argo CD installer](../../on-premises/k8s/argocd/install/argocd-install.sh)
- [Local Argo CD values](../../on-premises/k8s/argocd/install/values-local.yaml)
- [Development containers](../devcontainers/Development%20Containers.md)

## References

- [K3D documentation](https://k3d.io/stable/)
- [Argo CD Helm chart](https://github.com/argoproj/argo-helm/tree/argo-cd-10.9.3/charts/argo-cd)
- [Oh My Zsh](https://ohmyz.sh/)
