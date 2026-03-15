# 域名清单（速查）

| 域名 | 服务器 | 证书来源 | 续期方式 |
|-----|--------|----------|----------|
| www.xintuxiangce.top | root@web | letsencrypt live/www.xintuxiangce.top-0001 | cron 3:00 + 阿里云 DNS hook |
| m.xintuxiangce.top | 七牛 | 与 www 同证，在七牛上传 | 与 www 同证续期后到七牛更新 |
| xintuxiangce.top | root@web | 同上 | 同上 |
| www.aifuture.net.cn | root@web | letsencrypt live/aifuture.net.cn | cron 3:00，webroot |
| admin.xintuxiangce.top | root@web | letsencrypt live/admin.xintuxiangce.top | cron 3:00 |
| api.aifuture.net.cn | root@app | letsencrypt live/api.aifuture.net.cn | certbot-renew.timer，nginx |

- **web**：`ssh root@web`，lighttpd，cron 执行 `/usr/local/bin/certbot-renew-xintu.sh`。
- **app**：`ssh root@app`，nginx，systemd `certbot-renew.timer`。
