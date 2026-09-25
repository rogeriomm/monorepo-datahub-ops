```text
sudo apt install -y uidmap podman  podman-compose passt passt slirp4netns fuse-overlayfs
```

```shell
podman compose version
```

```shell
podman info --format '{{.Host.NetworkBackend}}'
```

```shell
podman run hello-world
```


- Install docker compose

```shell
sudo mkdir -p /usr/local/lib/docker/cli-plugins

sudo curl -L \
  https://github.com/docker/compose/releases/download/v5.5.1/docker-compose-linux-aarch64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose

sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

```shell
/usr/local/lib/docker/cli-plugins/docker-compose version
```

```shell
podman compose version
```


For rootless Podman as user `star` (UID 1000), enable the socket with:
```shell
systemctl --user enable --now podman.socket
```

```shell
systemctl --user status podman.socket
```

```shell
ls -l /run/user/1000/podman/podman.sock
```

