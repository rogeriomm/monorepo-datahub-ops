- Registry
```shell
dig harbor-registry.harbor.svc.cluster.local
```

```shell
nc -v harbor-registry.harbor.svc.cluster.local 5000
```

- https://harbor.ing.vm.world1l.worldl.xpt/
- https://harbor.ing.vm.world1l.worldl.xpt/v2


```shell
wget --no-check-certificate https://harbor.ing.vm.world1l.worldl.xpt/v2
```

 - Development only
```shell
cat /etc/docker/daemon.json
```
```json
{
  "insecure-registries": ["harbor.ing.vm.world1l.worldl.xpt"]
}
```

```shell
docker info | grep -A1 "Insecure Registries"
```

- Create user at https://harbor.ing.vm.world1l.worldl.xpt/harbor/users set as admin

```shell
docker login harbor.ing.vm.world1l.worldl.xpt
```

```shell
docker pull hello-world
docker image ls | grep hello-world
```

```shell
docker tag hello-world harbor.ing.vm.world1l.worldl.xpt/library/hello-world:latest
```

```shell
docker push harbor.ing.vm.world1l.worldl.xpt/library/hello-world:latest
```

```shell
docker pull harbor.ing.vm.world1l.worldl.xpt/library/hello-world:latest
```

# Default user name/password
- https://github.com/goharbor/harbor-helm/blob/ac65d7b4d6dd5f42b0e1521be2c488bc1663b1c4/values.yaml#L275

# Configure
## Docker
Copy the certificate to /etc/docker/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt

```shell
sudo mkdir -p /etc/docker/certs.d/harbor.ing.vm.pvel.worldl.xpt
sudo touch /etc/docker/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt
```

Edit /etc/docker/daemon.json. https://docs.docker.com/docker-hub/image-library/mirror/
```json
{
  "registry-mirrors": ["https://harbor.ing.vm.pvel.worldl.xpt"]
}
```

```shell
docker info | grep -A 2 "Registry Mirrors"
```


```shell
sudo systemctl restart docker
```

## K3S 
Copy the certificate to /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt

```shell
cat /etc/rancher/k3s/registries.yaml
```
```yaml
mirrors:
  "harbor.ing.vm.pvel.worldl.xpt":
    endpoint:
      - "https://harbor.ing.vm.pvel.worldl.xpt"
configs:
  "harbor.ing.vm.pvel.worldl.xpt":
    tls:
      ca_file: /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt
```
- For server nodes
```shell
sudo systemctl restart k3s
```

- For agent nodes
```shell
sudo systemctl restart k3s-agent
```

## K3S mirror
```shell
sudo mkdir -p /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt
sudo touch /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt
sudo touch /etc/rancher/k3s/registries.yaml
```

File /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt

File /etc/rancher/k3s/registries.yaml
```yaml
mirrors:
  # This new, specific rule tells K3s to ALWAYS get goharbor images
  # directly from Docker Hub, ignoring the general mirror below.
  "docker.io/goharbor":
    endpoint:
      - "https://registry-1.docker.io"

  # This is your general mirror rule for all other Docker Hub images.
  # K3s will only use this if a more specific rule doesn't match.
  docker.io:
    endpoint:
      - "https://harbor.ing.vm.pvel.worldl.xpt"

  # This is your existing entry for pulling from Harbor itself
  "harbor.ing.vm.pvel.worldl.xpt":
    endpoint:
      - "https://harbor.ing.vm.pvel.worldl.xpt"

configs:
  # This is your existing entry for trusting Harbor's certificate
  "harbor.ing.vm.pvel.worldl.xpt":
    tls:
      ca_file: /etc/rancher/k3s/certs.d/harbor.ing.vm.pvel.worldl.xpt/ca.crt
```

- For server nodes
```shell
sudo systemctl restart k3s
```

- For agent nodes
```shell
sudo systemctl restart k3s-agent
```

# Test
Create a project named "pub", enable "Proxy Cache" and "Public"


 - Edit /etc/docker/daemon.json
```json
{
  "insecure-registries": ["harbor.ing.vm.pvel.worldl.xpt"]
}
```
```shell
sudo systemctl restart docker
```

```shell
docker pull harbor.ing.vm.pvel.worldl.xpt/pub/nginx:latest
docker pull harbor.ing.vm.pvel.worldl.xpt/pub/apache/zeppelin:0.12.0
```

1 - Get the CA certificate from your Harbor instance.
2 - Copy the certificate to the trusted store on the current machine (e.g., /usr/local/share/ca-certificates/).
3 - Update the system's certificate list (e.g., with sudo update-ca-certificates).
4 - Restart the Docker service (sudo systemctl restart docker).

 - https://www.youtube.com/watch?v=sqC9bP8gwQ0

# Links 
   - https://github.com/goharbor/harbor-helm
   - https://docs.k3s.io/installation/private-registry
   - https://docs.docker.com/build/buildkit/configure/#setting-registry-certificates