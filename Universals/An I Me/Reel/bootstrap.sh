#!/bin/bash
SNAPSHOT=$1
MIN_NODES=$2

# Check Node Quorum
COUNT=$(check_node_health.py --active)
if [ "$COUNT" -lt "$MIN_NODES" ]; then
    exit 1
fi

# Broadcast to peers
NEW_EPOCH=$(date +%s)
broadcast_signal "BOOTSTRAP_INIT" --snapshot "$SNAPSHOT" --epoch "$NEW_EPOCH"