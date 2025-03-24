# Merge configs

- Rename context
```shell
KUBECONFIG=$HOME/.kube/config-vm.world1l.yaml kubectl config rename-context default world1l
KUBECONFIG=$HOME/.kube/config-vm.pvel.yaml kubectl config rename-context default pvel
KUBECONFIG=$HOME/.kube/config-vm.pve.yaml kubectl config rename-context default pve
```

```text
export KUBECONFIG=$HOME/.kube/config-vm.world1l.yaml:$HOME/.kube/config-vm.pvel.yaml:$HOME/.kube/config-vm.pve.yaml
```


# View cluster certificate
```shell
kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' > "$HOME/$(hostname)-kube-cert.txt"
```

```shell
base64 -d "$HOME/$(hostname)-kube-cert.txt" | openssl x509 -noout -text
```
   - Server certificate
```shell
openssl s_client -connect 127.0.0.1:6443 -showcerts </dev/null 2>/dev/null | openssl x509 -noout -text | grep -A1 "Subject Alternative Name"
```
```text
            X509v3 Subject Alternative Name: 
                DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster.local, DNS:localhost, DNS:vm.worldl1.worldl.xpt, IP Address:10.43.0.1, IP Address:127.0.0.1, IP Address:192.168.15.251, IP Address:2804:1B3:3080:4208:0:0:0:1D4C, IP Address:0:0:0:0:0:0:0:1
```


# Edit server certificate
   - https://docs.k3s.io/cli/server
   - Edit /etc/systemd/system/k3s, add line: '--tls-san=vm.world1l.worldl.xpt'
```Text
[Unit]
Description=Lightweight Kubernetes
Documentation=https://k3s.io
Wants=network-online.target
After=network-online.target

[Install]
WantedBy=multi-user.target

[Service]
Type=notify
EnvironmentFile=-/etc/default/%N
EnvironmentFile=-/etc/sysconfig/%N
EnvironmentFile=-/etc/systemd/system/k3s.service.env
KillMode=process
Delegate=yes
User=root
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
TimeoutStartSec=0
Restart=always
RestartSec=5s
ExecStartPre=/bin/sh -xc '! /usr/bin/systemctl is-enabled --quiet nm-cloud-setup.service 2>/dev/null'
ExecStartPre=-/sbin/modprobe br_netfilter
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/local/bin/k3s \
    server \
        '--flannel-backend=none' \
        '--cluster-cidr=10.250.0.0/16' \
        '--disable-network-policy' \
        '--disable=traefik' \
        '--tls-san=vm.world1l.worldl.xpt'
```

```shell
sudo systemctl daemon-reload
```

```shell
sudo systemctl restart k3s
```
