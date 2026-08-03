Most Proxmox cluster and datacenter configuration is exposed under /etc/pve

However, `/etc/pve` is not a normal directory. It is the `pmxcfs` cluster filesystem, backed by this SQLite database /var/lib/pve-cluster/config.db
