 sudo bridge -d link show master br0

#sudo bridge link set dev enp6s0 cost 100 # Ethernet 2.5Gb/sec
sudo bridge link set dev enp8s0 cost 2   # Ethernet 10Gb/sec

#
# br0 priority 8192
#
bridge_priority="$(ip -d link show br0 | grep -oP 'priority \K[0-9]+')"
echo "Bridge priority: ${bridge_priority}"


