#!/bin/bash
# 导出证书和私钥，用于上传到七牛云CDN

set -e

DOMAIN="download.xintuxiangce.top"
CERT_PATH="/etc/letsencrypt/live/$DOMAIN"

echo "=== 导出证书用于七牛云CDN ==="
echo ""

# 检查证书是否存在
if [ ! -d "$CERT_PATH" ]; then
    echo "❌ 证书不存在: $CERT_PATH"
    echo "   请先运行 request-download-cert.sh 申请证书"
    exit 1
fi

# 创建导出目录
EXPORT_DIR="/root/qiniu-cert-export"
mkdir -p $EXPORT_DIR

# 复制证书和私钥
echo "【导出证书文件】"
echo "----------------------------------------"
cp $CERT_PATH/fullchain.pem $EXPORT_DIR/certificate.pem
cp $CERT_PATH/privkey.pem $EXPORT_DIR/private.key

echo "✓ 证书已导出到: $EXPORT_DIR"
echo ""
ls -lh $EXPORT_DIR/
echo ""

# 显示证书内容（用于复制粘贴）
echo "【证书内容（用于上传到七牛云）】"
echo "----------------------------------------"
echo ""
echo "=== 证书内容 (certificate.pem) ==="
echo "（复制以下内容到七牛云CDN的证书输入框）"
echo ""
cat $EXPORT_DIR/certificate.pem
echo ""
echo ""
echo "=== 私钥内容 (private.key) ==="
echo "（复制以下内容到七牛云CDN的私钥输入框）"
echo ""
cat $EXPORT_DIR/private.key
echo ""

echo "【上传说明】"
echo "----------------------------------------"
echo "1. 登录七牛云CDN控制台"
echo "2. 找到域名: $DOMAIN"
echo "3. 进入「HTTPS配置」→「上传自有证书」"
echo "4. 证书内容: 复制上面的 certificate.pem 内容"
echo "5. 私钥内容: 复制上面的 private.key 内容"
echo "6. 保存配置"
echo ""
echo "或者直接使用导出的文件:"
echo "  scp $EXPORT_DIR/certificate.pem 本地路径/"
echo "  scp $EXPORT_DIR/private.key 本地路径/"

