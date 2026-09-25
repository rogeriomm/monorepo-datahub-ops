![[Pasted image 20260924160442.png|1019]]



```shell
sudo timedatectl set-timezone America/Sao_Paulo
sudo timedatectl set-ntp true
sudo locale-gen pt_BR.UTF-8
sudo update-locale LC_TIME=pt_BR.UTF-8
```

```shell
timedatectl status
timedatectl timesync-status
date
```


# Bugs
## Task state `No Status` indefinetly
Clock syncronization
```shell
sudo timedatectl set-ntp false
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
sleep 10
timedatectl timesync-status
```

Firewal open NTP, UDP por 123