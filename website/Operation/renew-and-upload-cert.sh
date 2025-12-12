#!/bin/bash
# 证书续期并自动上传到七牛云CDN（需要配置七牛云API）

set -e

DOMAIN="download.xintuxiangce.top"
CERT_PATH="/etc/letsencrypt/live/$DOMAIN"

echo "=== 证书续期并上传到七牛云 ==="
echo ""

# 续期证书
echo "【1. 续期证书】"
echo "----------------------------------------"
certbot renew --quiet --post-hook 'systemctl reload lighttpd'

if [ $? -eq 0 ]; then
    echo "✓ 证书续期成功"
else
    echo "❌ 证书续期失败"
    exit 1
fi
echo ""

# 导出证书
echo "【2. 导出证书】"
echo "----------------------------------------"
EXPORT_DIR="/root/qiniu-cert-export"
mkdir -p $EXPORT_DIR

cp $CERT_PATH/fullchain.pem $EXPORT_DIR/certificate.pem
cp $CERT_PATH/privkey.pem $EXPORT_DIR/private.key

echo "✓ 证书已导出到: $EXPORT_DIR"
echo ""

# 显示证书信息
echo "【3. 证书信息】"
echo "----------------------------------------"
openssl x509 -in $CERT_PATH/fullchain.pem -text -noout | grep -E 'Subject:|Not After' | head -2
echo ""

echo "【4. 下一步：手动上传到七牛云】"
echo "----------------------------------------"
echo "证书已更新，请手动上传到七牛云CDN:"
echo ""
echo "1. 登录七牛云CDN控制台"
echo "2. 找到域名: $DOMAIN"
echo "3. 进入「HTTPS配置」"
echo "4. 重新上传证书:"
echo "   - 证书: cat $EXPORT_DIR/certificate.pem"
echo "   - 私钥: cat $EXPORT_DIR/private.key"
echo ""
echo "或者查看证书内容:"
echo "  cat $EXPORT_DIR/certificate.pem"
echo "  cat $EXPORT_DIR/private.key"

