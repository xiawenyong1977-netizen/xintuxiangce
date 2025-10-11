# HTTPS 配置指南

## 📋 前置条件

在开始配置HTTPS之前，请确认：
- ✅ ICP备案已完成
- ✅ 已购买域名（如 xintuxiangce.com）
- ✅ 域名已完成实名认证
- ✅ 服务器正常运行（123.57.68.4）

## 🚀 方案选择

### 推荐方案：Cloudflare（免费 + 简单）

**优势**：
- 完全免费
- 自动SSL证书（自动续期）
- 全球CDN加速
- DDoS防护
- 配置简单

### 备选方案：Let's Encrypt（免费但需手动配置）

**优势**：
- 完全免费
- 直接在服务器配置
- 不依赖第三方

**劣势**：
- 需要定期手动续期（或配置自动续期）
- 没有CDN加速
- 没有额外防护

---

## 📘 方案一：使用 Cloudflare（推荐）

### 第一步：注册 Cloudflare

1. 访问：https://dash.cloudflare.com/sign-up
2. 注册免费账号
3. 验证邮箱

### 第二步：添加站点

1. 登录 Cloudflare Dashboard
2. 点击"添加站点"
3. 输入您的域名（如：xintuxiangce.com）
4. 选择"免费计划"
5. 点击"继续"

### 第三步：配置DNS记录

Cloudflare会扫描您现有的DNS记录，添加/修改以下记录：

```
类型: A
名称: @
内容: 123.57.68.4
代理状态: 已代理 ☁️（橙色云朵）
TTL: 自动

类型: A
名称: www
内容: 123.57.68.4
代理状态: 已代理 ☁️（橙色云朵）
TTL: 自动
```

### 第四步：更改域名服务器

Cloudflare会提供两个DNS服务器地址，例如：
```
aron.ns.cloudflare.com
lucy.ns.cloudflare.com
```

在您的域名注册商（阿里云/腾讯云）：
1. 登录域名管理后台
2. 找到DNS管理
3. 修改DNS服务器为Cloudflare提供的地址
4. 保存更改

等待DNS生效（通常几分钟到48小时）

### 第五步：配置SSL/TLS

1. 在 Cloudflare Dashboard 中进入您的站点
2. 点击左侧菜单"SSL/TLS"
3. 选择加密模式：**"灵活"**（推荐初始配置）

**加密模式说明**：
- **灵活**：用户到Cloudflare是HTTPS，Cloudflare到源服务器是HTTP
  - ✅ 最简单，无需配置源服务器
  - ✅ 立即可用
  - ⚠️ 源服务器到Cloudflare连接未加密

- **完全**：要求源服务器也有SSL证书
  - 稍复杂，需要在源服务器配置证书
  - 更安全

- **完全（严格）**：要求源服务器有有效的SSL证书
  - 最安全
  - 配置最复杂

### 第六步：配置其他优化（可选）

#### 自动HTTPS重写
1. SSL/TLS → 边缘证书
2. 开启"始终使用HTTPS"
3. 开启"自动HTTPS重写"

#### 缓存配置
1. 缓存 → 配置
2. 缓存级别：标准
3. 浏览器缓存TTL：4小时

#### 性能优化
1. 速度 → 优化
2. 开启"自动缩小"（HTML、CSS、JS）
3. 开启"Brotli"压缩

### 第七步：更新网站配置

连接服务器并更新robots.txt和sitemap.xml：

```bash
ssh root@123.57.68.4

# 更新 robots.txt
cd /var/www/xintuxiangce
sed -i 's/your-domain.com/xintuxiangce.com/g' robots.txt
sed -i 's/http:/https:/g' robots.txt

# 更新 sitemap.xml
sed -i 's/your-domain.com/xintuxiangce.com/g' sitemap.xml
sed -i 's/http:/https:/g' sitemap.xml

# 重启服务
systemctl restart lighttpd
```

### 第八步：添加ICP备案号

编辑网站底部，添加备案号：

```bash
ssh root@123.57.68.4
cd /var/www/xintuxiangce
nano index.html
```

在 footer-bottom 部分添加：
```html
<div class="footer-bottom">
    <p>&copy; 2025 芯图相册. 保留所有权利.</p>
    <p><a href="https://beian.miit.gov.cn/" target="_blank">京ICP备XXXXXXXX号</a></p>
    <p class="footer-tagline">让照片管理更智能，让隐私更安全</p>
</div>
```

### 第九步：测试

1. 访问：https://xintuxiangce.com
2. 检查SSL证书（浏览器地址栏有锁图标）
3. 测试所有功能：
   - 导航链接
   - 图片加载
   - 下载功能
   - 响应式布局

### 第十步：强制HTTPS（推荐）

确认网站正常后，强制所有HTTP请求跳转到HTTPS：

在 Cloudflare 中：
1. SSL/TLS → 边缘证书
2. 开启"始终使用HTTPS"

---

## 📘 方案二：使用 Let's Encrypt

### 第一步：配置域名DNS

在域名注册商后台添加A记录：
```
类型: A
主机记录: @
记录值: 123.57.68.4

类型: A
主机记录: www
记录值: 123.57.68.4
```

等待DNS生效（可用 `nslookup xintuxiangce.com` 检查）

### 第二步：安装 Certbot

```bash
ssh root@123.57.68.4

# 安装certbot
yum install -y certbot

# 或者使用snap安装（推荐）
yum install -y snapd
systemctl enable --now snapd.socket
snap install core
snap refresh core
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
```

### 第三步：停止 Lighttpd（临时）

```bash
systemctl stop lighttpd
```

### 第四步：申请证书

```bash
# 替换为您的域名和邮箱
certbot certonly --standalone \
  -d xintuxiangce.com \
  -d www.xintuxiangce.com \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email
```

证书将保存在：
- 证书：`/etc/letsencrypt/live/xintuxiangce.com/fullchain.pem`
- 私钥：`/etc/letsencrypt/live/xintuxiangce.com/privkey.pem`

### 第五步：配置 Lighttpd SSL

创建SSL配置：

```bash
cat > /etc/lighttpd/conf.d/ssl.conf << 'EOF'
# SSL配置
server.modules += ( "mod_openssl" )

$SERVER["socket"] == ":443" {
    ssl.engine = "enable"
    ssl.pemfile = "/etc/letsencrypt/live/xintuxiangce.com/fullchain.pem"
    ssl.privkey = "/etc/letsencrypt/live/xintuxiangce.com/privkey.pem"
    
    # 现代化SSL配置
    ssl.cipher-list = "ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384"
    ssl.honor-cipher-order = "enable"
    ssl.dh-file = "/etc/ssl/certs/dhparam.pem"
    ssl.use-sslv2 = "disable"
    ssl.use-sslv3 = "disable"
}
EOF

# 生成DH参数（这需要几分钟）
openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

# 给证书目录设置权限
chmod 755 /etc/letsencrypt/live
chmod 755 /etc/letsencrypt/archive
```

### 第六步：更新主配置

编辑 `/etc/lighttpd/lighttpd.conf`，确保包含SSL配置：

```bash
echo 'include "conf.d/ssl.conf"' >> /etc/lighttpd/lighttpd.conf
```

### 第七步：配置HTTP到HTTPS跳转

```bash
cat >> /etc/lighttpd/lighttpd.conf << 'EOF'

# HTTP跳转到HTTPS
$HTTP["scheme"] == "http" {
    url.redirect = ("" => "https://${url.authority}${url.path}${qsa}")
}
EOF
```

### 第八步：测试并启动

```bash
# 测试配置
lighttpd -t -f /etc/lighttpd/lighttpd.conf

# 启动服务
systemctl start lighttpd

# 检查状态
systemctl status lighttpd
```

### 第九步：配置自动续期

Let's Encrypt证书有效期90天，需要定期续期：

```bash
# 测试续期
certbot renew --dry-run

# 设置自动续期（添加到crontab）
echo "0 3 * * * certbot renew --quiet --post-hook 'systemctl reload lighttpd'" | crontab -
```

---

## 🧪 测试清单

配置完成后，请检查：

- [ ] https://您的域名.com 可以访问
- [ ] http://您的域名.com 自动跳转到HTTPS
- [ ] www子域名正常工作
- [ ] 浏览器地址栏显示锁图标
- [ ] 所有图片正常加载
- [ ] 下载功能正常
- [ ] 移动端显示正常
- [ ] 使用SSL Labs测试：https://www.ssllabs.com/ssltest/

## 🔧 故障排查

### 问题1：证书未生效
```bash
# 检查lighttpd错误日志
tail -f /var/log/lighttpd/error.log

# 检查证书文件
ls -la /etc/letsencrypt/live/您的域名/
```

### 问题2：无法访问443端口
```bash
# 检查防火墙
firewall-cmd --list-all
firewall-cmd --add-service=https --permanent
firewall-cmd --reload

# 检查端口监听
netstat -tlnp | grep 443
```

### 问题3：混合内容警告
- 检查HTML中所有链接都使用HTTPS
- 或使用相对路径
- 或在Cloudflare中开启"自动HTTPS重写"

## 📊 两种方案对比

| 特性 | Cloudflare | Let's Encrypt |
|------|-----------|---------------|
| **费用** | 免费 | 免费 |
| **配置难度** | ⭐⭐ 简单 | ⭐⭐⭐⭐ 复杂 |
| **CDN加速** | ✅ 有 | ❌ 无 |
| **DDoS防护** | ✅ 有 | ❌ 无 |
| **自动续期** | ✅ 自动 | ⚠️ 需配置 |
| **证书类型** | Universal SSL | Let's Encrypt |
| **配置时间** | 10分钟 | 30分钟 |

## 💡 推荐建议

**强烈推荐使用 Cloudflare 方案**，因为：
- 配置更简单
- 提供免费CDN加速
- 自动SSL续期，无需维护
- 额外的安全防护
- 隐藏真实服务器IP

---

## 📞 配置完成后

配置成功后，请：
1. 提交网站到搜索引擎（Google、百度）
2. 更新所有推广链接为HTTPS
3. 添加网站统计代码
4. 监控网站性能和安全性

## 🎉 恭喜！

完成上述步骤后，您的芯图相册官网将拥有：
- ✅ 专业域名
- ✅ HTTPS安全连接
- ✅ CDN全球加速（如使用Cloudflare）
- ✅ 完整的SEO优化
- ✅ 合规的ICP备案

您的网站已经达到生产级别标准！

