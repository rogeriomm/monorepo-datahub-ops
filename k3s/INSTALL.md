   * https://docs.tigera.io/calico/latest/getting-started/kubernetes/k3s/quickstart

```shell
curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--flannel-backend=none --cluster-cidr=10.250.0.0/16 --disable-network-policy --disable=traefik" sh -
```

```shell
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
```

# Install NGINX Ingress
```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.5/deploy/static/provider/cloud/deploy.yaml
```