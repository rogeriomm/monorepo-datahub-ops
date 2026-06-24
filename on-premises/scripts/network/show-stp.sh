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


watch "figlet $HOSTNAME && \
     sudo brctl showstp $MONITOR_BRIDGE"
