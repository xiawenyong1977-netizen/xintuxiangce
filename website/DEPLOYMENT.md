# 部署指南

本文档提供了芯图相册官网的详细部署说明。

## 📋 部署前准备

### 1. 文件检查
确保以下文件存在且路径正确：
- [x] index.html
- [x] styles.css
- [x] script.js
- [x] robots.txt
- [x] sitemap.xml
- [x] .htaccess (Apache 服务器)
- [x] ../icons/imageclassify.png
- [x] ../images/*.jpg
- [x] ../dist/芯图相册-智能分类，便捷管理，仅你可见 1.0.0.exe

### 2. 更新配置
在部署前，需要修改以下内容：

#### robots.txt
```txt
Sitemap: https://your-domain.com/sitemap.xml
```
将 `your-domain.com` 替换为您的实际域名。

#### sitemap.xml
```xml
<loc>https://your-domain.com/</loc>
```
将所有 `your-domain.com` 替换为您的实际域名。

#### index.html（可选）
如果需要，可以添加：
- Google Analytics 跟踪代码
- 百度统计代码
- 其他分析工具

## 🚀 部署方案

### 方案一：静态托管平台（推荐新手）

#### Vercel（推荐）
1. 注册 Vercel 账号：https://vercel.com
2. 安装 Vercel CLI：
   ```bash
   npm i -g vercel
   ```
3. 在 website 目录下运行：
   ```bash
   cd website
   vercel
   ```
4. 按照提示完成部署

**优点**：
- 免费
- 自动 HTTPS
- 全球 CDN 加速
- 自动部署

#### Netlify
1. 注册 Netlify 账号：https://netlify.com
2. 将 website 文件夹拖拽到 Netlify Drop
3. 或使用 Netlify CLI：
   ```bash
   npm install -g netlify-cli
   netlify deploy
   ```

**优点**：
- 免费
- 自动 HTTPS
- 持续集成
- 表单处理

#### GitHub Pages
1. 创建 GitHub 仓库
2. 上传 website 文件夹内容到仓库
3. 在仓库设置中启用 GitHub Pages
4. 选择分支和文件夹

**优点**：
- 免费
- 与 GitHub 集成
- 自动部署

### 方案二：云服务器

#### 阿里云/腾讯云
1. 购买云服务器（ECS）
2. 安装 Nginx 或 Apache
3. 配置域名和 DNS
4. 上传文件到服务器
5. 配置 SSL 证书（推荐使用 Let's Encrypt）

**Nginx 配置示例**：
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL 证书配置
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # 网站根目录
    root /var/www/xintuxiangce;
    index index.html;
    
    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
    
    # 缓存配置
    location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location ~* \.(css|js)$ {
        expires 1M;
        add_header Cache-Control "public";
    }
    
    # 安全头部
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # 404 页面（可选）
    error_page 404 /404.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 方案三：Docker 部署

创建 `Dockerfile`：
```dockerfile
FROM nginx:alpine

# 复制网站文件
COPY . /usr/share/nginx/html/

# 复制 Nginx 配置（可选）
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

构建和运行：
```bash
docker build -t xintuxiangce-website .
docker run -d -p 80:80 xintuxiangce-website
```

## 🔧 优化配置

### 1. 图片优化

#### 压缩图片
使用工具压缩图片：
- TinyPNG: https://tinypng.com
- ImageOptim (Mac)
- Squoosh: https://squoosh.app

#### 转换为 WebP 格式
```bash
# 安装 cwebp
apt-get install webp  # Ubuntu/Debian
brew install webp     # macOS

# 转换图片
cwebp -q 80 input.jpg -o output.webp
```

在 HTML 中使用：
```html
<picture>
    <source srcset="image.webp" type="image/webp">
    <img src="image.jpg" alt="Description">
</picture>
```

### 2. CSS/JS 压缩

#### 使用在线工具
- CSS: https://cssminifier.com
- JS: https://javascript-minifier.com

#### 使用构建工具
```bash
# 安装 csso-cli 和 terser
npm install -g csso-cli terser

# 压缩 CSS
csso styles.css -o styles.min.css

# 压缩 JS
terser script.js -o script.min.js -c -m
```

更新 HTML 引用：
```html
<link rel="stylesheet" href="styles.min.css">
<script src="script.min.js"></script>
```

### 3. CDN 加速

#### 使用 CDN 托管静态资源
推荐服务：
- 阿里云 CDN
- 腾讯云 CDN
- Cloudflare（国际）
- 七牛云
- 又拍云

配置步骤：
1. 注册 CDN 服务
2. 添加加速域名
3. 配置源站
4. 更新 DNS 记录
5. 开启 HTTPS

### 4. 性能监控

#### Google PageSpeed Insights
https://pagespeed.web.dev

#### GTmetrix
https://gtmetrix.com

#### WebPageTest
https://www.webpagetest.org

## 📊 SEO 配置

### 1. 百度站长工具
1. 注册：https://ziyuan.baidu.com
2. 验证网站所有权
3. 提交 sitemap.xml
4. 主动推送 URL

### 2. Google Search Console
1. 注册：https://search.google.com/search-console
2. 验证网站所有权
3. 提交 sitemap.xml
4. 检查索引状态

### 3. 添加统计代码

#### Google Analytics
在 `</head>` 前添加：
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

#### 百度统计
在 `</head>` 前添加：
```html
<!-- 百度统计 -->
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?YOUR_SITE_ID";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
```

## 🔒 安全配置

### 1. SSL 证书

#### Let's Encrypt (免费)
```bash
# 安装 certbot
apt-get install certbot python3-certbot-nginx

# 自动配置 Nginx
certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
certbot renew --dry-run
```

#### 阿里云/腾讯云 SSL
在云服务商控制台申请免费 SSL 证书

### 2. 防火墙配置
```bash
# UFW (Ubuntu)
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 3. 定期备份
- 备份网站文件
- 备份配置文件
- 使用版本控制（Git）

## 📱 移动端优化

### 1. 测试工具
- Chrome DevTools
- Mobile-Friendly Test: https://search.google.com/test/mobile-friendly

### 2. 优化建议
- 确保所有交互元素足够大（至少 44x44px）
- 测试不同设备和屏幕尺寸
- 优化触摸交互

## ✅ 部署检查清单

部署后请检查以下项目：

- [ ] 网站可以正常访问
- [ ] HTTPS 正常工作
- [ ] 所有图片正常显示
- [ ] 下载链接有效
- [ ] 导航链接正常
- [ ] 响应式布局正常
- [ ] FAQ 折叠功能正常
- [ ] 截图标签切换正常
- [ ] 移动端菜单正常
- [ ] 返回顶部按钮正常
- [ ] 表单提交正常（如有）
- [ ] robots.txt 可访问
- [ ] sitemap.xml 可访问
- [ ] 404 页面配置（可选）
- [ ] 统计代码正常工作
- [ ] SEO 标签正确
- [ ] 页面加载速度
- [ ] 跨浏览器测试

## 🔄 持续维护

### 定期任务
- 每周检查网站可用性
- 每月检查 SSL 证书有效期
- 每季度更新应用截图和版本号
- 定期查看统计数据
- 及时更新内容

### 性能监控
- 设置 Uptime 监控
- 使用 Lighthouse 定期测试
- 关注 Core Web Vitals

### 内容更新
- 添加新功能介绍
- 更新 FAQ
- 发布更新日志（可选）
- 添加用户案例（可选）

## 📞 故障排查

### 常见问题

1. **图片无法显示**
   - 检查图片路径是否正确
   - 检查文件权限
   - 检查图片文件是否存在

2. **CSS/JS 不生效**
   - 清除浏览器缓存
   - 检查文件路径
   - 查看浏览器控制台错误

3. **下载链接无效**
   - 确认文件存在
   - 检查文件路径
   - 检查服务器 MIME 类型配置

4. **移动端布局错误**
   - 检查响应式断点
   - 测试不同设备
   - 查看浏览器兼容性

## 📚 参考资源

- [MDN Web Docs](https://developer.mozilla.org/)
- [Google SEO 指南](https://developers.google.com/search/docs)
- [Web.dev](https://web.dev/)
- [Nginx 文档](https://nginx.org/en/docs/)

---

**最后更新**: 2025年10月11日

如有问题，请参考 README.md 或联系技术支持。

