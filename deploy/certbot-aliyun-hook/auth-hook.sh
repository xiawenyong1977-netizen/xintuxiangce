#!/bin/bash
# Certbot manual-auth-hook: add TXT via Aliyun DNS API
# Reads ALY_KEY and ALY_TOKEN from /etc/letsencrypt/aksk.ini

set -e
AKSK="/etc/letsencrypt/aksk.ini"
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -f "$AKSK" ]; then
  echo "Missing $AKSK (Aliyun AccessKey)" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$AKSK"
python3 "$HOOK_DIR/alydns.py" add "$CERTBOT_DOMAIN" "_acme-challenge" "$CERTBOT_VALIDATION" "$ALY_KEY" "$ALY_TOKEN"
# Wait for DNS propagation
sleep 25
