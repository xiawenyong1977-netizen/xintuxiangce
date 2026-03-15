#!/bin/bash
# Certbot manual-cleanup-hook: remove TXT via Aliyun DNS API

set -e
AKSK="/etc/letsencrypt/aksk.ini"
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
[ -f "$AKSK" ] || exit 0
# shellcheck disable=SC1090
source "$AKSK"
python3 "$HOOK_DIR/alydns.py" clean "$CERTBOT_DOMAIN" "_acme-challenge" "$CERTBOT_VALIDATION" "$ALY_KEY" "$ALY_TOKEN"
