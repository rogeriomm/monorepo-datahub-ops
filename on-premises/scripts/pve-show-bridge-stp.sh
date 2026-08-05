#!/usr/bin/env zsh

get_interface_hardware_name() {
    local interface="$1"
    local vendor
    local device


    if [[ -z "$interface" ]]; then
        echo "Usage: get_interface_hardware_name <interface>"
        return 1
    fi

    if [[ ! -d "/sys/class/net/$interface" ]]; then
        echo "Interface not found: $interface"
        return 1
    fi

    vendor=$(sudo ethtool -i "$interface" 2>/dev/null |
        awk -F': ' '/^driver:/ {print $2}')

    device=$(sudo lshw -class network 2>/dev/null |
        awk -v iface="$interface" '
            /logical name:/ {
                current = $3
            }
            current == iface && /product:/ {
                sub(/^[[:space:]]*product:[[:space:]]*/, "")
                print
                exit
            }
        ')

    echo  "# Hardware name of interface $interface" | gum format
    if [[ -n "$device" ]]; then
        echo "$device"
    elif [[ -n "$vendor" ]]; then
        echo "$vendor"
    else
        echo "Unknown hardware"
        return 1
    fi
}

is_stp_forwarding() {
    local interface="$1"

    if sudo bridge link show dev "$interface" 2>/dev/null |
        grep -qw 'state forwarding'; then
        echo "$interface: forwarding"
        return 0
    else
        echo "$interface: not forwarding"
        return 1
    fi
}




is_stp_forwarding fwln100i0
is_stp_forwarding  fwln102i0

get_interface_hardware_name eno1
get_interface_hardware_name ens6f1 

sudo brctl show vmbr1

echo "# 10Gb - ens6f1" | gum format
sudo ethtool ens6f1 | grep -E 'Speed:|Link detected:'
is_stp_forwarding ens6f1

echo "# 1Gb - eno1" | gum format
sudo ethtool eno1 | grep -E 'Speed:|Link detected:'
is_stp_forwarding eno1 

print -P "# Bridge vmbr1:\n$(sudo ifconfig vmbr1 | grep inet)" | gum format

echo "# Bridge vmbr1 STP priority: $(ip -d link show vmbr1 | grep -oP 'bridge.*priority \K[0-9]+')" | gum format

echo "# Bridge vmbr1 STP: \n $(sudo brctl showstp vmbr1)" | gum format

