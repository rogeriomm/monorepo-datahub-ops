# pve
Proxmox 8.4

# pvel
Proxmox 8.4 

# world1l
Fedora 42
 - /etc/NetworkManager/system-connections/enp6s0.nmconnection
```text
 [connection]
id=enp6s0
uuid=03ebdbd1-175a-4f4b-afb7-3ef8f3be95a1
type=ethernet
autoconnect-priority=99
controller=a8a22594-de42-4d3e-b240-956063af871e
port-type=bridge

[ethernet]
mac-address=74:56:3C:E2:96:5C

[bridge-port]
path-cost=100
priority=32
```

- /etc/NetworkManager/system-connections/enp7s0.nmconnection
```text
[connection]
id=enp7s0
uuid=c4ae4f77-866e-4395-9b00-611efc0d84a7
type=ethernet
autoconnect-priority=2
controller=a8a22594-de42-4d3e-b240-956063af871e
port-type=bridge

[ethernet]
mac-address=02:76:C6:01:52:AF

[bridge-port]
path-cost=50
priority=32
```