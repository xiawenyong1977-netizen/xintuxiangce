---
name: domain-ssl-renewal-check
description: Check SSL certificate expiry and renewal configuration for project domains (xintuxiangce.top, aifuture.net.cn). Use when the user asks to check domain expiry, certificate expiration, renewal config, or SSL status for these domains.
---

# 域名证书与续期配置检查

本技能记录项目相关域名的证书与续期配置，并指导如何手工检查**到期时间**与**续期配置是否正常**。

## 域名与服务器一览

| 域名 | 服务器 | Web | 证书名/路径 | 验证方式 | 续期后重载 |
|-----|--------|-----|-------------|----------|------------|
| www.xintuxiangce.top | root@web | lighttpd | www.xintuxiangce.top-0001 | manual + dns-01（阿里云 hook） | renew_hook reload lighttpd |
| m.xintuxiangce.top | 七牛 CDN | - | 与 www 同证，需在七牛上传 | 同上（同证） | 七牛控制台更新证书 |
| xintuxiangce.top | root@web | lighttpd | www.xintuxiangce.top-0001 | 同上 | renew_hook |
| www.aifuture.net.cn | root@web | lighttpd | aifuture.net.cn | webroot | renew_hook reload lighttpd |
| admin.xintuxiangce.top | root@web | lighttpd | admin.xintuxiangce.top | （见服务器） | - |
| api.aifuture.net.cn | root@app | nginx | api.aifuture.net.cn | nginx 插件 | certbot-renew.timer / nginx 插件 |

- **root@web**：lighttpd，证书目录 `/etc/letsencrypt/live/`，续期脚本 `/usr/local/bin/certbot-renew-xintu.sh`，cron 每天 3 点。
- **root@app**：nginx，certbot 使用 systemd 定时器 `certbot-renew.timer`（约每 12 小时），无 PRE/POST_HOOK 时由 nginx 插件负责重载。

## 检查一：域名证书到期时间

### 方式 A：从本机拉取公网证书（推荐，无需 SSH）

对任意域名执行（将 `DOMAIN` 换成要查的域名，如 `https://www.xintuxiangce.top`）：

```powershell
$req = [System.Net.HttpWebRequest]::Create("https://DOMAIN")
$req.Timeout = 15000
try { $req.GetResponse().Close() } catch {}
$cert = $req.ServicePoint.Certificate
Write-Host "Subject: $($cert.Subject)"
Write-Host "NotBefore: $($cert.GetEffectiveDateString())"
Write-Host "NotAfter: $($cert.GetExpirationDateString())"
```

一次查多个域名可循环：

```powershell
@("https://www.xintuxiangce.top", "https://m.xintuxiangce.top", "https://www.aifuture.net.cn", "https://api.aifuture.net.cn") | ForEach-Object {
  $req = [System.Net.HttpWebRequest]::Create($_)
  $req.Timeout = 15000
  try { $req.GetResponse().Close() } catch {}
  $c = $req.ServicePoint.Certificate
  Write-Host "$_ -> NotAfter: $($c.GetExpirationDateString())"
}
```

### 方式 B：在服务器上看 certbot 状态

**root@web：**

```bash
ssh root@web "certbot certificates"
```

关注每个 Certificate Name 的 `Expiry Date` 和 `(VALID: N days)`。

**root@app：**

```bash
ssh root@app "certbot certificates"
```

## 检查二：续期配置是否正常

### root@web（lighttpd）

1. **定时任务**  
   ```bash
   ssh root@web "crontab -l"
   ```  
   应包含：`0 3 * * * /usr/local/bin/certbot-renew-xintu.sh >> /var/log/certbot-renew.log 2>&1`

2. **续期脚本**  
   ```bash
   ssh root@web "cat /usr/local/bin/certbot-renew-xintu.sh"
   ```  
   应为：`certbot renew --non-interactive`（不停止 lighttpd，以便 webroot 验证）。

3. **xintuxiangce 证书（DNS-01）**  
   ```bash
   ssh root@web "grep -E 'manual_auth_hook|manual_cleanup_hook|renew_hook' /etc/letsencrypt/renewal/www.xintuxiangce.top-0001.conf"
   ```  
   应有：`manual_auth_hook`、`manual_cleanup_hook` 指向阿里云 hook，以及 `renew_hook = systemctl reload lighttpd`。

4. **阿里云 hook 与密钥**  
   ```bash
   ssh root@web "ls -la /etc/letsencrypt/aliyun-dns-hook/auth-hook.sh /etc/letsencrypt/aksk.ini"
   ```  
   `aksk.ini` 存在且权限 600，内容为有效阿里云 AccessKey。

5. **aifuture（webroot）**  
   ```bash
   ssh root@web "grep renew_hook /etc/letsencrypt/renewal/aifuture.net.cn.conf"
   ```  
   应有：`renew_hook = systemctl reload lighttpd`。

### root@app（nginx）

1. **定时器**  
   ```bash
   ssh root@app "systemctl list-timers certbot-renew.timer"
   ```  
   应显示 certbot-renew.timer 已启用且下次运行时间合理。

2. **api.aifuture 续期配置**  
   ```bash
   ssh root@app "cat /etc/letsencrypt/renewal/api.aifuture.net.cn.conf"
   ```  
   应有 `authenticator = nginx`。若需显式重载 nginx，可加：`renew_hook = systemctl reload nginx`。

3. **可选：全局 hook**  
   ```bash
   ssh root@app "grep -E 'POST_HOOK|DEPLOY_HOOK' /etc/sysconfig/certbot"
   ```  
   若为空，续期后重载依赖 nginx 插件或各证书的 renew_hook。

## 检查结果怎么算“正常”

- **到期时间**：所有域名 NotAfter 均在将来，且距离到期 ≥ 7 天为佳；&lt; 30 天应关注是否很快会触发自动续期。
- **续期配置**：  
  - web：cron 存在、脚本为 `certbot renew --non-interactive`，xintuxiangce 有阿里云 hook + renew_hook，aifuture 有 renew_hook。  
  - app：certbot-renew.timer 启用，api 证书为 nginx 插件且必要时有 renew_hook 或 POST_HOOK。

## 参考

- 阿里云 DNS hook 脚本与说明：项目内 `deploy/certbot-aliyun-hook/`，示例密钥 `aksk.ini.example`。
- 部署与服务器信息：`.cursor/rules/deployment.mdc`（root@web 与网站目录）。
