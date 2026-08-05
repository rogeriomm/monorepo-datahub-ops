#!/usr/bin/env zsh

# Usage:
#   ./check-stp-state.zsh <interface>
#
# Example:
#   ./check-stp-state.zsh eno1

interface="${1:-}"

if [[ -z "$interface" ]]; then
    echo "Usage: $0 <interface>"
    exit 1
fi

if [[ ! -d "/sys/class/net/$interface" ]]; then
    echo "Error: interface '$interface' does not exist."
    exit 2
fi

stp_state=$(bridge link show dev "$interface" 2>/dev/null \
    | sed -n 's/.*state \([^ ]*\).*/\1/p' \
    | head -n 1)

case "$stp_state" in
    forwarding)
        print -P "%F{green}✓ $interface is in the STP forwarding state.%f"
        exit 0
        ;;
    blocking|listening|learning|disabled)
        print -P "%F{yellow}⚠ $interface is in the STP state: $stp_state%f"
        exit 1
        ;;
    "")
        print -P "%F{red}✗ Could not determine the STP state for $interface.%f"
        print "The interface may not belong to a Linux bridge."
        exit 2
        ;;
    *)
        print -P "%F{yellow}⚠ $interface has an unknown STP state: $stp_state%f"
        exit 3
        ;;
esac

