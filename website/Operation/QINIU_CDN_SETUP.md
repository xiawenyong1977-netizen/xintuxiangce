# 七牛云CDN配置指南

本文档提供七牛云对象存储 + CDN 的完整配置步骤，用于加速安装包下载。

## 📋 前置准备

1. **注册七牛云账号**
   - 访问：https://www.qiniu.com
   - 完成实名认证（必需）

2. **安装Python依赖**
   
   **在服务器 123.57.68.4 上安装**（用于上传脚本）:
   ```bash
   ssh root@123.57.68.4
   pip3 install qiniu
   # 或者
   python3 -m pip install qiniu
   ```
   
   **注意**: 上传脚本 `qiniu-upload.py` 需要在服务器上运行，因为它需要访问服务器上的 `/var/www/xintuxiangce/dist/` 目录。

## 🔧 配置步骤

### 步骤1: 创建对象存储空间（Bucket）

1. 登录七牛云控制台
2. 进入「对象存储」→「空间管理」
3. 点击「新建空间」
4. 配置信息：
   - **空间名称**: `xintuxiangce-downloads`
   - **存储区域**: 选择「华东」（或根据用户分布选择）
   - **访问控制**: 选择「公开空间」（下载需要公开访问）
   - **CDN加速**: 勾选「开启CDN加速」
5. 点击「确定」创建

### 步骤2: 获取Access Key和Secret Key

1. 进入「个人中心」→「密钥管理」
2. 查看或创建 Access Key 和 Secret Key
3. **重要**: 妥善保管密钥，不要泄露

### 步骤3: 配置本地配置文件

1. 复制配置文件模板：
   ```bash
   cp qiniu-config.json.example qiniu-config.json
   ```

2. 编辑 `qiniu-config.json`，填写以下信息：
   ```json
   {
     "access_key": "你的AccessKey",
     "secret_key": "你的SecretKey",
     "bucket_name": "xintuxiangce-downloads",
     "domain": "https://download.xintuxiangce.top",
     "region": "z0",
     "base_path": "dist",
     "cdn_enabled": true,
     "fallback_to_source": true
   }
   ```

   **说明**:
   - `access_key`: 七牛云 Access Key
   - `secret_key`: 七牛云 Secret Key
   - `bucket_name`: 对象存储空间名称
   - `domain`: CDN加速域名（需要先配置CDN）
   - `region`: 存储区域代码（华东: z0, 华北: z1, 华南: z2）
   - `cdn_enabled`: 是否启用CDN
   - `fallback_to_source`: CDN不可用时是否回退到源站

### 步骤4: 配置CDN加速域名

**推荐方案：使用子域名分离**

只对下载文件使用CDN，页面保留在源站，这样更新更简单。

1. 进入「CDN」→「域名管理」
2. 点击「添加域名」
3. 配置信息：
   - **加速域名**: `m.xintuxiangce.top`（推荐使用，因为证书已包含该域名）
   - **备选**: `download.xintuxiangce.top`（需要单独申请证书）
   - **源站配置**: 
     - 源站类型: 选择「七牛云对象存储」
     - 空间名称: `xintuxiangce-downloads`
   - **缓存配置**: 
     - 大文件（.zip, .exe, .apk）: 缓存30天
     - 其他文件: 缓存7天（实际上只有安装包，可以都设30天）
   - **缓存参数**: 选择「忽略所有参数」（重要！）
     - 原因: 安装包下载URL通常没有参数，忽略参数可提高缓存命中率
4. 点击「创建」

**重要说明**:
- ✅ **主域名 `www.xintuxiangce.top` 不配置CDN**，直接指向源站服务器
- ✅ 这样HTML页面、CSS、JS、图片都在源站，更新简单
- ✅ 只有下载文件通过 `download.xintuxiangce.top` 走CDN加速
- ✅ 页面更新时不需要刷新CDN缓存

### 步骤5: 配置DNS解析

需要配置两个域名的DNS解析：

**1. 主域名（不经过CDN）**:
   - **记录类型**: A
   - **主机记录**: `www`（或 `@` 表示主域名）
   - **记录值**: 源站服务器IP（`123.57.68.4`）
   - **TTL**: 600（或默认值）
   - **说明**: 主域名直接指向源站，不经过CDN

**2. 下载域名（经过CDN）**:
   - **记录类型**: CNAME
   - **主机记录**: `m`（使用 `m.xintuxiangce.top` 作为下载域名）
   - **记录值**: 七牛云提供的CNAME地址（在CDN控制台查看，如：`m.xintuxiangce.top.w.kunlunea.com`）
   - **TTL**: 600（或默认值）
   - **说明**: 下载域名通过CNAME指向CDN
   - **注意**: 使用 `m.xintuxiangce.top` 的好处是证书已包含该域名，无需单独申请证书

等待DNS生效（通常几分钟到几小时）

### 步骤6: 配置HTTPS证书

**推荐方案：使用现有证书（如果使用 m.xintuxiangce.top）**

✅ **好消息**：您现有的证书已包含 `m.xintuxiangce.top`，可以直接使用，无需申请新证书！

**配置步骤**：

#### 6.1 导出现有证书（如果使用 m.xintuxiangce.top）

在服务器上执行以下命令导出证书：

```bash
ssh root@123.57.68.4

# 查看证书信息（确认包含 m.xintuxiangce.top）
openssl x509 -in /etc/letsencrypt/live/www.xintuxiangce.top/fullchain.pem -text -noout | grep 'DNS:'

# 查看证书内容（用于复制）
cat /etc/letsencrypt/live/www.xintuxiangce.top/fullchain.pem

# 查看私钥内容（用于复制）
cat /etc/letsencrypt/live/www.xintuxiangce.top/privkey.pem
```

#### 6.1b 申请新证书（如果使用 download.xintuxiangce.top）

**如果使用 download.xintuxiangce.top**，需要单独申请证书：

1. **上传证书申请脚本到服务器**:
   ```bash
   scp request-download-cert.sh root@123.57.68.4:/root/
   scp export-cert-for-qiniu.sh root@123.57.68.4:/root/
   ```

2. **SSH到服务器并执行**:
   ```bash
   ssh root@123.57.68.4
   chmod +x /root/request-download-cert.sh
   chmod +x /root/export-cert-for-qiniu.sh
   ```

3. **编辑脚本，设置邮箱**:
   ```bash
   nano /root/request-download-cert.sh
   # 修改 EMAIL="your-email@example.com" 为您的邮箱
   ```

4. **执行证书申请**:
   ```bash
   /root/request-download-cert.sh
   ```
   - 选择验证方式：推荐选择 `1`（HTTP-01验证）
   - 如果 lighttpd 正在运行，脚本会提示临时停止（验证完成后会自动重启）

5. **导出证书**:
   ```bash
   /root/export-cert-for-qiniu.sh
   ```
   - 脚本会显示证书和私钥内容，方便复制

#### 6.2 上传证书到七牛云CDN

1. 登录七牛云CDN控制台
2. 找到域名 `download.xintuxiangce.top`
3. 点击「HTTPS配置」
4. 选择「上传自有证书」
5. 填写证书信息：
   - **证书内容**: 复制 `export-cert-for-qiniu.sh` 输出的证书内容（certificate.pem）
   - **私钥内容**: 复制 `export-cert-for-qiniu.sh` 输出的私钥内容（private.key）
6. 开启「强制HTTPS跳转」（可选，推荐开启）
7. 保存配置
8. 等待证书生效（通常几分钟到几小时）

#### 6.3 配置证书自动续期

Let's Encrypt证书有效期90天，需要定期续期：

```bash
# 测试续期
certbot renew --dry-run

# 设置自动续期（添加到crontab）
echo "0 3 * * * certbot renew --quiet --post-hook 'systemctl reload lighttpd'" | crontab -
```

**注意**: 证书续期后，需要重新导出并上传到七牛云CDN。可以创建一个续期后自动上传的脚本。

**重要说明**：
- ✅ CDN域名的证书只需要在CDN控制台配置，**不需要在源站服务器配置**
- ✅ 源站服务器（`www.xintuxiangce.top`）的证书保持不变
- ✅ 两个域名可以分别使用不同的证书，互不影响
- ⚠️ 证书需要定期续期（90天），续期后需要重新上传到CDN

### 步骤7: 上传文件到对象存储

1. **将上传脚本和配置文件复制到服务器**:
   ```bash
   # 从本地复制到服务器
   scp qiniu-upload.py root@123.57.68.4:/root/
   scp qiniu-config.json root@123.57.68.4:/root/
   ```

2. **在服务器上运行上传脚本**:
   ```bash
   ssh root@123.57.68.4
   cd /root
   python3 qiniu-upload.py
   ```
   
   **注意**: 确保服务器上已安装 `qiniu` 库（见前置准备步骤2）

3. 脚本会自动：
   - 扫描 `/var/www/xintuxiangce/dist/` 目录
   - 找到所有安装包文件
   - 上传到七牛云对象存储
   - 保持目录结构（pc/portable/, pc/setup/, android/）

3. 上传完成后，检查文件是否可访问：
   ```bash
   curl -I https://download.xintuxiangce.top/pc/portable/xtxc202510151254.zip
   ```

### 步骤8: 更新下载脚本

1. 将 `download-cdn.py` 复制到服务器：
   ```bash
   scp website/download-cdn.py root@123.57.68.4:/var/www/xintuxiangce/website/
   ```

2. 将配置文件复制到服务器：
   ```bash
   scp qiniu-config.json root@123.57.68.4:/var/www/xintuxiangce/website/
   ```

3. 设置执行权限：
   ```bash
   ssh root@123.57.68.4 "chmod +x /var/www/xintuxiangce/website/download-cdn.py"
   ```

4. 备份原文件并替换：
   ```bash
   ssh root@123.57.68.4 "cd /var/www/xintuxiangce/website && cp download.py download.py.backup && cp download-cdn.py download.py"
   ```

5. 配置Lighttpd支持Python CGI（如果还没有）：
   - 确保 `mod_cgi` 已启用
   - 确保 `.py` 文件有执行权限

## 🔄 文件更新流程

### 页面更新（简单）

由于页面保留在源站，更新非常简单：

1. **直接更新服务器文件**:
   ```bash
   scp website/index.html root@123.57.68.4:/var/www/xintuxiangce/website/
   ```

2. **立即生效**:
   - 不需要刷新CDN缓存
   - 用户访问立即看到最新内容
   - 无需等待

### 安装包更新

当有新版本安装包时：

1. **上传新文件到七牛云**:
   ```bash
   ssh root@123.57.68.4
   cd /root
   python3 qiniu-upload.py
   ```

2. **刷新CDN缓存**（可选，新文件会自动缓存）:
   - 在CDN控制台 → 缓存刷新 → 添加需要刷新的URL
   - 或等待缓存自动过期（30天）

3. **验证下载**:
   - 访问下载链接测试: `https://download.xintuxiangce.top/pc/portable/xxx.zip`
   - 检查下载速度

## 📊 监控和维护

### 查看使用统计

1. 进入「CDN」→「统计分析」
2. 查看：
   - 流量使用情况
   - 请求次数
   - 命中率
   - 下载速度

### 设置流量告警

1. 进入「费用中心」→「告警设置」
2. 设置流量告警阈值（如50GB/月）
3. 配置告警通知方式

### 成本优化建议

1. **图片压缩**: 上传前压缩图片，减少流量
2. **版本管理**: 定期清理旧版本文件
3. **缓存优化**: 合理设置缓存时间
4. **监控流量**: 定期检查异常流量

## 🐛 故障排查

### CDN不可用时的回退

脚本已配置自动回退到源站，如果CDN不可用，会自动从源站下载。

### 检查CDN配置

```bash
# 检查CDN域名是否可访问
curl -I https://download.xintuxiangce.top/pc/portable/test.zip

# 检查DNS解析
nslookup download.xintuxiangce.top

# 检查CDN缓存状态
curl -I -H "Cache-Control: no-cache" https://download.xintuxiangce.top/pc/portable/test.zip
```

### 常见问题

1. **403 Forbidden**
   - 检查对象存储空间是否为「公开空间」
   - 检查文件权限设置

2. **404 Not Found**
   - 检查文件是否已上传
   - 检查文件路径是否正确

3. **下载速度慢**
   - 检查CDN节点是否正常
   - 检查源站带宽
   - 考虑升级CDN套餐

## 📝 配置文件说明

### qiniu-config.json

```json
{
  "access_key": "七牛云AccessKey",
  "secret_key": "七牛云SecretKey",
  "bucket_name": "对象存储空间名称",
  "domain": "CDN加速域名",
  "region": "存储区域代码",
  "base_path": "本地文件基础路径",
  "cdn_enabled": true,
  "fallback_to_source": true
}
```

## 🔒 安全建议

1. **保护密钥**: 不要将 `qiniu-config.json` 提交到Git仓库
2. **使用环境变量**: 生产环境建议使用环境变量存储密钥
3. **配置防盗链**: 在CDN控制台配置Referer白名单
4. **定期更新**: 定期更换Access Key和Secret Key

## 📞 技术支持

- 七牛云文档: https://developer.qiniu.com/
- 七牛云工单: https://support.qiniu.com/

