# Install
- Install mise tool
  - https://mise.jdx.dev/getting-started.html


```shell
git clone https://github.com/rogeriomm/monorepo-datahub-ops
```

```shell
cd monorepo-datahub-ops
```

```shell
mise install
```

# NFS server setup
## vm.worldl1.worldl.xpt
  - cat /etc/exports
```text
# 192.168.15.251 vm.worldl1.worldl.xpt
/mnt/data/nfs 192.168.15.251(rw,sync,no_subtree_check,no_root_squash,fsid=1)
/mnt/data/git 192.168.15.251(rw,sync,no_subtree_check,no_root_squash,fsid=2)
```
```shell
sudo exportfs -v
```
```text
/mnt/data/nfs 	192.168.15.251(sync,wdelay,hide,no_subtree_check,fsid=1,sec=sys,rw,secure,no_root_squash,no_all_squash)
/mnt/data/git 	192.168.15.251(sync,wdelay,hide,no_subtree_check,fsid=2,sec=sys,rw,secure,no_root_squash,no_all_squash)
```

- Testing
```shell
sudo mount -t nfs -o nfsvers=4.2 vm.worldl1.worldl.xpt:/mnt/data/git /tmp/git
```
