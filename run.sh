#!/bin/bash

echo "Starting Docker Compose..."
docker compose up --build 2>&1 | tee compose.log | while read -r line; do
    # Look for the Cloudflare tunnel URL
    if [[ "$line" =~ https://[a-zA-Z0-9-]+\.trycloudflare\.com ]]; then
        TUNNEL_URL="${BASH_REMATCH[0]}"
        echo ""
        echo "======================================"
        echo " 🌐 Tunnel URL Detected!"
        echo " $TUNNEL_URL"
        echo "======================================"
        echo ""
        echo "$TUNNEL_URL" > tunnel_url.txt
    fi

    # Also display docker compose logs to user
    echo "$line"
done
