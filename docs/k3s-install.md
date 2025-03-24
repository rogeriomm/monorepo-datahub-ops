## Install K3S
### Install K3S
  - world1l
```shell
curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--flannel-backend=none --cluster-cidr=10.250.0.0/16 --disable-network-policy --disable=traefik" sh -
```  
  - vm.pvel
```shell
curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--flannel-backend=none --cluster-cidr=10.251.0.0/16 --disable-network-policy --disable=traefik" sh -
```

- vm.pve
```shell  
curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" INSTALL_K3S_EXEC="--flannel-backend=none --cluster-cidr=10.252.0.0/16 --disable-network-policy --disable=traefik" sh -
```


### Configure
```shell
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config.yaml
sudo chown $USER:$USER ~/.kube/config.yaml
```

```shell
sudo unlink /usr/local/bin/kubectl 
```


### Check
```shell
kubectl get pods
```
```text
kubectl get nodes
NAME                 STATUS     ROLES                  AGE     VERSION
vm.pvel.worldl.xpt   NotReady   control-plane,master   3m37s   v1.32.3+k3s1
```

### Configure k3s/global limits
- Edit add lines
```shell
sudo systemctl edit k3s
```

```plain text
[Service]
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
LimitNOFILE=infinity
TasksMax=infinity
```

- Reload configuration
```shell
sudo systemctl daemon-reload
sudo systemctl restart k3s
```

- Check limits
```shell
sudo cat /proc/$(pidof k3s)/limits
```
```plain text
Limit                     Soft Limit           Hard Limit           Units     
Max cpu time              unlimited            unlimited            seconds   
Max file size             unlimited            unlimited            bytes     
Max data size             unlimited            unlimited            bytes     
Max stack size            8388608              unlimited            bytes     
Max core file size        unlimited            unlimited            bytes     
Max resident set          unlimited            unlimited            bytes     
Max processes             unlimited            unlimited            processes 
Max open files            1000000              1000000              files     
Max locked memory         8388608              8388608              bytes     
Max address space         unlimited            unlimited            bytes     
Max file locks            unlimited            unlimited            locks     
Max pending signals       353217               353217               signals   
Max msgqueue size         819200               819200               bytes     
Max nice priority         0                    0                    
Max realtime priority     0                    0                    
Max realtime timeout      unlimited            unlimited            us 
```


```shell
sysctl fs.inotify.max_user_watches
sysctl fs.inotify.max_user_instances
sysctl fs.inotify.max_queued_events
```

- Edit, add lines
```shell
sudo vim /etc/security/limits.conf
```

```text
root  soft  nofile  unlimited
root  hard  nofile  unlimited
root  soft  nproc   unlimited
root  hard  nproc   unlimited
root  soft  core    unlimited
root  hard  core    unlimited
```
- Reload
```shell
sudo systemctl daemon-reexec
sudo systemctl restart k3s
```



- Run
```shell
sudo tee /etc/sysctl.d/99-k3s.conf > /dev/null <<EOF
fs.file-max=2097152
fs.inotify.max_user_watches=1048576
fs.inotify.max_user_instances=8192
EOF
``` 
- Apply
```shell
sudo sysctl --system
```

- Reboot machine
```shell
sudo reboot
```

- Check limits
```shell
sudo cat /proc/$(pidof k3s)/limits
```


- Check limits
```shell
ps -ef | grep k3s
```

```shell
sudo cat /proc/$(pidof k3s)/limits
```



# Install Calico
   - https://docs.tigera.io/calico/latest/getting-started/kubernetes/k3s/quickstart
```shell
kubectl get installations default -o yaml | yq
```


### Calico operator
```shell
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.0/manifests/operator-crds.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.0/manifests/tigera-operator.yaml
```

```shell
kubectl apply -f ./custom-resources.yaml
```

```shell
kubectl get -n calico-apiserver networkpolicies/allow-apiserver -o yaml | yq
```

# Install NGINX Ingress
   - https://github.com/kubernetes/ingress-nginx
      - https://github.com/kubernetes/ingress-nginx?tab=readme-ov-file#supported-versions-table

   - Check the kubernetes version     
```shell
kubectl version
```

   - Using https://github.com/kubernetes/ingress-nginx?tab=readme-ov-file#supported-versions-table set the NGINX ingress version
```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.2/deploy/static/provider/cloud/deploy.yaml
```


# Install load balancer
Install HAProxy
- https://docs.k3s.io/datastore/cluster-loadbalancer









# TRASH FIXME

# ArgoCD
- https://bitnami.com/stack/argo-cd/helm

# TODO
```shell
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

# Check installation
```shell
kubectl exec -n argocd deploy/argocd-repo-server -- ls -la
```


```shell
argocd admin initial-password -n argocd
```

```shell
argocd login --insecure argocd.vm.pvel.worldl.xpt
```

# Remove stuck application
- Edit
```shell
kubectl edit application harbor -n argocd
```

- Remove the finalizers block, it will look like

```yaml
finalizers:
  - resources-finalizer.argocd.argoproj.io
```

This will immediately allow Kubernetes to delete the stuck Application resource.

# Create ArgoCD application
1. Create namespace manually
2. Create the ArgoCD Application

Warning: You MUST create the namespace manually first

# Kubectl contexts
```shell
kubectl config set-context k8s-argocd-context \
  --cluster=default \
  --user=default \
  --namespace=argocd
```

```shell
kubectl config get-contexts
```

```shell
kubectl config use-context k8s-argocd-context
```

```shell
kubectl --context=k8s-argocd-context get pods
```

# Issues
## Too many redirects
- https://github.com/argoproj/argo-cd/issues/2953
```shell
curl -kIL https://argocd.vm.world1l.worldl.xpt
```
## ArgoCD OOMKill
```shell
kubectl -n argo-cd set resources deployment argo-cd-app-controller \
  --containers=controller \
  --requests=memory=512Mi \
  --limits=memory=1Gi
```

```shell
sudo dmesg
```

# Edit server certificates
[Multicluster](multicluster.md)

# Links
- https://docs.tigera.io/calico/latest/getting-started/kubernetes/k3s/quickstart
- https://kubernetes.io/docs/concepts/services-networking/network-policies/
