# 安装PHP支持（可选）

如果您想让网站自动检测并下载最新的zip文件，需要安装PHP。

## 安装步骤

### 1. 安装PHP和PHP-FPM

```bash
ssh root@123.57.68.4

# 安装PHP和必要的扩展
yum install -y php php-fpm php-cli

# 启动PHP-FPM服务
systemctl start php-fpm
systemctl enable php-fpm

# 检查PHP版本
php -v
```

### 2. 配置Lighttpd支持PHP

```bash
# 安装lighttpd的FastCGI模块
yum install -y lighttpd-fastcgi

# 创建PHP配置
cat > /etc/lighttpd/conf.d/php.conf << 'EOF'
server.modules += ( "mod_fastcgi" )

fastcgi.server = (
    ".php" => ((
        "socket" => "/var/run/php-fpm/php-fpm.sock",
        "broken-scriptfilename" => "enable"
    ))
)
EOF

# 在主配置中包含PHP配置
echo 'include "conf.d/php.conf"' >> /etc/lighttpd/lighttpd.conf
```

### 3. 配置PHP-FPM

编辑 `/etc/php-fpm.d/www.conf`，确保以下设置：

```ini
user = lighttpd
group = lighttpd
listen = /var/run/php-fpm/php-fpm.sock
listen.owner = lighttpd
listen.group = lighttpd
listen.mode = 0660
```

### 4. 重启服务

```bash
# 重启PHP-FPM
systemctl restart php-fpm

# 测试配置
lighttpd -t -f /etc/lighttpd/lighttpd.conf

# 重启Lighttpd
systemctl restart lighttpd

# 检查服务状态
systemctl status php-fpm
systemctl status lighttpd
```

### 5. 测试PHP

创建测试文件：

```bash
echo "<?php phpinfo(); ?>" > /var/www/xintuxiangce/test.php
```

访问：http://123.57.68.4/test.php

如果看到PHP信息页面，说明配置成功。

### 6. 更新下载链接

修改 `index.html` 中的下载按钮：

```html
<a href="download.php" class="btn btn-primary btn-large download-btn">
```

`download.php` 文件已经上传到服务器，它会自动：
- 优先选择 `.zip` 文件
- 如果没有zip文件，则选择 `.exe` 文件
- 自动选择最新的文件（按修改时间）

### 7. 测试下载

```bash
# 测试下载脚本
curl http://localhost/download.php?info

# 应该返回类似这样的JSON：
# {"success":true,"filename":"xtxc202510111614.zip","size":287578021,"sizeFormatted":"274.30 MB","extension":"zip","modifiedTime":"2025-10-11 16:14:02"}
```

## 优势

安装PHP后的优势：
- ✅ 完全自动化，无需手动更新配置
- ✅ 上传新zip文件后立即生效
- ✅ 自动选择最新文件
- ✅ 自动显示文件大小和版本信息

## 当前方案（JavaScript）

如果不安装PHP，当前的JavaScript方案也完全够用：
- ✅ 简单易用
- ✅ 无需额外配置
- ✅ 性能更好（纯静态）
- ⚠️ 需要手动更新配置文件

## 建议

- **个人/小型项目**：使用当前的JavaScript方案即可
- **频繁更新版本**：建议安装PHP，省去手动配置的麻烦
- **高访问量网站**：保持纯静态（JavaScript方案）性能更好

