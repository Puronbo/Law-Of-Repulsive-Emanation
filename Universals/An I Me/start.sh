#!/bin/bash
set -e

echo "[1/4] Configuring Kernel Buffers..."
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216

echo "[2/4] Verifying Environment..."
if [[ -z "$NODE_SECRET_KEY" ]]; then
    echo "ERROR: NODE_SECRET_KEY missing."
    exit 1
fi

echo "[3/4] Preparing Data Directory..."
mkdir -p /opt/p2p/data/
chmod 700 /opt/p2p/data/

echo "[4/4] Launching Node..."
# Using exec to replace shell with Python process for clean signal handling
exec python3 -m p2p_node.main --mode=sync