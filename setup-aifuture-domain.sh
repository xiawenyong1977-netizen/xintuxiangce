#!/bin/bash
# 配置 www.aifuture.net.cn 域名的脚本
# 此脚本将配置 lighttpd 虚拟主机，使 www.aifuture.net.cn 显示 aifuture.html 作为首页

echo "正在配置 www.aifuture.net.cn 虚拟主机..."

# 复制配置文件到 lighttpd 配置目录
cp aifuture-vhost.conf /etc/lighttpd/conf.d/aifuture-vhost.conf

# 检查主配置文件是否已包含此配置
if ! grep -q "conf.d/aifuture-vhost.conf" /etc/lighttpd/lighttpd.conf; then
    echo "include \"conf.d/aifuture-vhost.conf\"" >> /etc/lighttpd/lighttpd.conf
    echo "已添加配置到主配置文件"
else
    echo "配置已在主配置文件中"
fi

# 测试配置
echo "正在测试 lighttpd 配置..."
lighttpd -t -f /etc/lighttpd/lighttpd.conf

if [ $? -eq 0 ]; then
    echo "配置测试通过！"
    echo "正在重启 lighttpd 服务..."
    systemctl restart lighttpd
    echo "配置完成！"
    echo ""
    echo "请确保："
    echo "1. DNS 已配置：www.aifuture.net.cn 和 aifuture.net.cn 的 A 记录指向服务器 IP"
    echo "2. SSL 证书已配置（如果需要 HTTPS）"
    echo "3. 访问 http://www.aifuture.net.cn 测试"
else
    echo "配置测试失败，请检查错误信息"
    exit 1
fi

