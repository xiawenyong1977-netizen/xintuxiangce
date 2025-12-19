#!/bin/bash
# Lighttpd URL规范化配置脚本
# 用于配置301重定向：HTTP→HTTPS, 非www→www, index.html→/

echo "=========================================="
echo "Lighttpd URL规范化配置"
echo "=========================================="
echo ""

# 备份配置文件
CONFIG_FILE="/etc/lighttpd/lighttpd.conf"
BACKUP_FILE="/etc/lighttpd/lighttpd.conf.backup.$(date +%Y%m%d_%H%M%S)"

echo "1. 备份配置文件..."
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "   备份文件: $BACKUP_FILE"
echo ""

# 检查是否已存在重定向配置
if grep -q "URL规范化配置" "$CONFIG_FILE"; then
    echo "⚠️  检测到已存在URL规范化配置"
    read -p "是否要覆盖现有配置？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "已取消操作"
        exit 1
    fi
    # 删除旧的配置
    sed -i '/# URL规范化配置/,/^$/d' "$CONFIG_FILE"
fi

echo "2. 添加URL规范化配置..."
cat >> "$CONFIG_FILE" << 'EOF'

# URL规范化配置 - 强制HTTPS和www
$HTTP["host"] =~ "^(xintuxiangce\.top|www\.xintuxiangce\.top)$" {
    # HTTP → HTTPS
    $HTTP["scheme"] == "http" {
        url.redirect = (
            "^/(.*)" => "https://www.xintuxiangce.top/$1"
        )
    }
    
    # 非www → www (HTTPS)
    $HTTP["scheme"] == "https" {
        $HTTP["host"] =~ "^xintuxiangce\.top$" {
            url.redirect = (
                "^/(.*)" => "https://www.xintuxiangce.top/$1"
            )
        }
    }
}

# 移除index.html
url.redirect = (
    "^/index\.html$" => "/",
    "^/index\.html\?(.*)$" => "/?$1"
)
EOF

echo "   ✅ 配置已添加"
echo ""

echo "3. 测试配置文件..."
if lighttpd -t -f "$CONFIG_FILE"; then
    echo "   ✅ 配置文件语法正确"
else
    echo "   ❌ 配置文件语法错误，正在恢复备份..."
    cp "$BACKUP_FILE" "$CONFIG_FILE"
    exit 1
fi
echo ""

echo "4. 重启Lighttpd服务..."
if systemctl restart lighttpd; then
    echo "   ✅ Lighttpd已重启"
else
    echo "   ❌ 重启失败，请手动检查"
    exit 1
fi
echo ""

echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "验证重定向："
echo "  curl -I http://xintuxiangce.top/"
echo "  curl -I https://xintuxiangce.top/"
echo "  curl -I https://www.xintuxiangce.top/index.html"
echo ""
echo "如果看到 Location: https://www.xintuxiangce.top/ 说明配置成功"
echo ""

