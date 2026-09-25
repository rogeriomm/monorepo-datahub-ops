```shell
#!/bin/sh

PREREQ=""

prereqs()
{
    echo "$PREREQ"
}

case "$1" in
    prereqs)
        prereqs
        exit 0
        ;;
esac

echo "Orange Pi 5: waiting for PCI rescan interface" > /dev/kmsg

# Wait up to 5 seconds for PCI sysfs to become available
i=0
while [ ! -e /sys/bus/pci/rescan ] && [ "$i" -lt 50 ]; do
    sleep 0.1
    i=$((i + 1))
done

if [ -e /sys/bus/pci/rescan ]; then
    echo "Orange Pi 5: rescanning PCI bus" > /dev/kmsg
    echo 1 > /sys/bus/pci/rescan
else
    echo "Orange Pi 5: /sys/bus/pci/rescan not available" > /dev/kmsg
fi

exit 0

```

```shell
sudo chmod +x /etc/initramfs-tools/scripts/init-premount/nvme-rescan
sudo update-initramfs -u
```

```shell
lsinitramfs /boot/initrd.img-$(uname -r) | grep nvme-rescan
```