# Diagnose and repair Orange Pi 5 Armbian boot

# Maskrom mode

```shell
sudo dnf install -y rkdeveloptool
```

```shell
sudo rkdeveloptool ld
```

![[Pasted image 20260923121724.png|1056]]

![[Pasted image 20260923121856.png|1054]]
# NVME

![[Pasted image 20260924105609.png|1222]]


# Creating microSD installer
```shell
IMAGE=$1
echo "Image: $IMAGE"
xzcat "$IMAGE" | sudo dd \
    of=/dev/sda \
    bs=4M \
    iflag=fullblock \
    status=progress \
    conv=fsync
```

# Updating the u-boot
```
armbian-install
```
# Issues
## No NVME controller on PCI bus
- https://forum.armbian.com/topic/49225-orange-pi-5-unable-to-detect-nvme-drive/
```shell
echo 1 | sudo tee /sys/bus/pci/rescan
```

# Links
 - https://orangepi.net/wp-content/uploads/2024/09/OrangePi_5_RK3588S_User-Manual_v2.1.1.pdf
 - https://armbian.com/boards/orangepi5
 - https://armbian.atomonetworks.com/dl/orangepi5/archive/
 - https://rsync.armbian.com/
	 - https://rsync.armbian.com/oldarchive/orangepi5/archive/

