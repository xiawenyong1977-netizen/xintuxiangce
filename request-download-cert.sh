#!/bin/bash
# 为 download.xintuxiangce.top 申请 Let's Encrypt 证书

set -e

DOMAIN="download.xintuxiangce.top"
EMAIL="your-email@example.com"  # 请替换为您的邮箱

echo "=== 为 $DOMAIN 申请 Let's Encrypt 证书 ==="
echo ""

# 检查 certbot 是否安装
if ! command -v certbot &> /dev/null; then
    echo "❌ certbot 未安装，正在安装..."
    yum install -y certbot || apt-get update && apt-get install -y certbot
fi

# 检查域名DNS解析
echo "【1. 检查域名DNS解析】"
echo "----------------------------------------"
if dig +short $DOMAIN | grep -q .; then
    echo "✓ 域名 $DOMAIN 已解析"
    dig +short $DOMAIN
else
    echo "⚠️  警告: 域名 $DOMAIN 可能未正确解析"
    echo "   请确保域名已添加A记录指向服务器IP: 123.57.68.4"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# 检查80端口是否可用（HTTP验证需要）
echo "【2. 检查80端口】"
echo "----------------------------------------"
if netstat -tlnp | grep -q ':80 '; then
    echo "✓ 80端口已被占用（可能是lighttpd）"
    echo "  将使用 HTTP-01 验证方式"
    VALIDATION_METHOD="standalone"
else
    echo "⚠️  80端口未被占用"
    echo "  将使用 standalone 模式（需要临时停止lighttpd）"
    VALIDATION_METHOD="standalone"
fi
echo ""

# 选择验证方式
echo "【3. 选择验证方式】"
echo "----------------------------------------"
echo "1. HTTP-01 验证（需要域名指向服务器，推荐）"
echo "2. DNS-01 验证（需要手动添加DNS记录）"
read -p "请选择验证方式 (1/2): " -n 1 -r
echo
echo ""

if [[ $REPLY =~ ^[1]$ ]]; then
    # HTTP-01 验证
    echo "【使用 HTTP-01 验证】"
    echo "----------------------------------------"
    echo "注意: 如果 lighttpd 正在运行，需要临时停止"
    echo ""
    
    # 检查 lighttpd 状态
    if systemctl is-active --quiet lighttpd; then
        echo "⚠️  lighttpd 正在运行，需要临时停止"
        read -p "是否现在停止 lighttpd？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            systemctl stop lighttpd
            echo "✓ lighttpd 已停止"
            RESTART_LIGHTTPD=true
        else
            echo "❌ 无法继续，请手动停止 lighttpd 后重试"
            exit 1
        fi
    fi
    
    # 申请证书
    echo ""
    echo "正在申请证书..."
    certbot certonly --standalone \
        -d $DOMAIN \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        --non-interactive || {
        echo "❌ 证书申请失败"
        if [ "$RESTART_LIGHTTPD" = true ]; then
            systemctl start lighttpd
        fi
        exit 1
    }
    
    # 重启 lighttpd
    if [ "$RESTART_LIGHTTPD" = true ]; then
        echo ""
        echo "正在重启 lighttpd..."
        systemctl start lighttpd
        echo "✓ lighttpd 已重启"
    fi
    
elif [[ $REPLY =~ ^[2]$ ]]; then
    # DNS-01 验证
    echo "【使用 DNS-01 验证】"
    echo "----------------------------------------"
    echo "注意: 需要手动添加DNS TXT记录"
    echo ""
    
    # 申请证书（DNS验证）
    certbot certonly --manual --preferred-challenges dns \
        -d $DOMAIN \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        --manual-public-ip-logging-ok || {
        echo "❌ 证书申请失败"
        exit 1
    }
else
    echo "❌ 无效的选择"
    exit 1
fi

# 显示证书信息
echo ""
echo "【4. 证书申请成功】"
echo "----------------------------------------"
CERT_PATH="/etc/letsencrypt/live/$DOMAIN"
if [ -d "$CERT_PATH" ]; then
    echo "✓ 证书已保存到: $CERT_PATH"
    echo ""
    echo "证书文件:"
    ls -lh $CERT_PATH/
    echo ""
    echo "证书信息:"
    openssl x509 -in $CERT_PATH/fullchain.pem -text -noout | grep -E 'Subject:|Issuer:|DNS:|Not Before|Not After' | head -10
    echo ""
    echo "【5. 证书文件路径】"
    echo "----------------------------------------"
    echo "证书文件: $CERT_PATH/fullchain.pem"
    echo "私钥文件: $CERT_PATH/privkey.pem"
    echo ""
    echo "【6. 下一步：上传到七牛云CDN】"
    echo "----------------------------------------"
    echo "1. 登录七牛云CDN控制台"
    echo "2. 找到域名: $DOMAIN"
    echo "3. 进入「HTTPS配置」"
    echo "4. 选择「上传自有证书」"
    echo "5. 上传以下文件内容:"
    echo "   - 证书内容: cat $CERT_PATH/fullchain.pem"
    echo "   - 私钥内容: cat $CERT_PATH/privkey.pem"
    echo ""
    echo "或者使用以下命令查看证书内容:"
    echo "  cat $CERT_PATH/fullchain.pem"
    echo "  cat $CERT_PATH/privkey.pem"
else
    echo "❌ 证书目录不存在"
    exit 1
fi

