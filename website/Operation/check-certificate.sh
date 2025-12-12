#!/bin/bash
# 检查当前域名的HTTPS证书信息

echo "=== 检查HTTPS证书信息 ==="
echo ""

# 方法1: 查找证书文件位置
echo "【1. 查找证书文件位置】"
echo "----------------------------------------"
grep -r 'ssl.pemfile\|ssl.cert-file' /etc/lighttpd/conf.d/ /etc/lighttpd/lighttpd.conf 2>/dev/null | head -5
echo ""

# 方法2: 检查常见的证书位置
echo "【2. 检查常见证书位置】"
echo "----------------------------------------"
CERT_PATHS=(
    "/etc/letsencrypt/live/xintuxiangce.top/fullchain.pem"
    "/etc/letsencrypt/live/www.xintuxiangce.top/fullchain.pem"
    "/etc/ssl/certs/xintuxiangce.top.crt"
    "/etc/ssl/certs/www.xintuxiangce.top.crt"
)

for cert_path in "${CERT_PATHS[@]}"; do
    if [ -f "$cert_path" ]; then
        echo "✓ 找到证书: $cert_path"
        echo ""
        echo "【证书详细信息】"
        echo "----------------------------------------"
        openssl x509 -in "$cert_path" -text -noout | grep -E 'Subject:|Issuer:|DNS:|Not Before|Not After' | head -20
        echo ""
        echo "【证书包含的域名（Subject Alternative Name）】"
        echo "----------------------------------------"
        openssl x509 -in "$cert_path" -text -noout | grep -A 1 "Subject Alternative Name" | grep -oP 'DNS:\K[^,]+' || echo "未找到SAN信息"
        echo ""
        break
    fi
done

# 方法3: 通过在线查看
echo "【3. 在线查看证书信息】"
echo "----------------------------------------"
echo "可以通过以下方式在线查看证书:"
echo "  - https://www.ssllabs.com/ssltest/analyze.html?d=www.xintuxiangce.top"
echo "  - https://crt.sh/?q=xintuxiangce.top"
echo ""

# 方法4: 通过curl查看远程证书
echo "【4. 查看远程证书信息】"
echo "----------------------------------------"
echo | openssl s_client -servername www.xintuxiangce.top -connect www.xintuxiangce.top:443 2>/dev/null | openssl x509 -noout -text | grep -E 'Subject:|Issuer:|DNS:|Not Before|Not After' | head -20

