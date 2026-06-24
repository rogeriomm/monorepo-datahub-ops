#!/bin/zsh

# Usage: ./set_bridge_priority.sh <priority>
# Example: ./set_bridge_priority.sh 1000

# Check argument
if [[ -z "$1" ]]; then
  echo "Usage: $0 <priority>"
  exit 1
fi

PRIORITY="$1"
BRIDGE="vmbr1"

# Detect hostname
HOSTNAME="$(hostname)"

# Map host to monitoring bridge
case "$HOSTNAME" in
  world1l.worldl.xpt)
    MONITOR_BRIDGE="br0"
    ;;
  pve.worldl.xpt)
    MONITOR_BRIDGE="vmbr1"
    ;;
  pvel.worldl.xpt)
    MONITOR_BRIDGE="vmbr0"
    ;;
  *)
    echo "Unknown host: $HOSTNAME"
    exit 1
    ;;
esac

# Apply bridge priority
sudo ip link set dev "$BRIDGE" type bridge priority "$PRIORITY" || {
  echo "❌ Failed to set priority on $BRIDGE"
  exit 1
}

# Monitor STP status
watch -n 2 "
  figlet $HOSTNAME PRIORITY:$PRIORITY
  echo '===================='
  echo 'Bridge Info ($MONITOR_BRIDGE)'
  echo '--------------------'
  sudo brctl show $MONITOR_BRIDGE
  echo '--------------------'
  echo 'STP State ($MONITOR_BRIDGE)'
  echo '--------------------'
  sudo brctl showstp $MONITOR_BRIDGE
  echo '===================='
"
