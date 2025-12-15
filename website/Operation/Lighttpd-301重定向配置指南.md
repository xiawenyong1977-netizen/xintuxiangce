# Lighttpd 301重定向配置指南

## 📋 配置目标

将旧的使用指南链接重定向到新链接：
- `/guide-quick-start.html` → `/guides/quick-start.html`
- `/guide-permissions.html` → `/guides/permissions.html`
- `/guide-cleanup.html` → `/guides/cleanup.html`
- `/guide-multidimensional-classification.html` → `/guides/multidimensional-classification.html`

## 🔧 配置方法

### 方法一：在主配置文件中添加（推荐）

编辑 Lighttpd 主配置文件（通常是 `/etc/lighttpd/lighttpd.conf`），添加以下配置：

```lighttpd
# 使用指南旧链接301重定向
$HTTP["host"] == "www.xintuxiangce.top" {
    url.redirect = (
        "^/guide-quick-start\.html$" => "/guides/quick-start.html",
        "^/guide-permissions\.html$" => "/guides/permissions.html",
        "^/guide-cleanup\.html$" => "/guides/cleanup.html",
        "^/guide-multidimensional-classification\.html$" => "/guides/multidimensional-classification.html"
    )
}
```

### 方法二：使用正则表达式（更简洁）

如果Lighttpd版本支持，可以使用正则表达式匹配所有guide-*.html：

```lighttpd
# 使用指南旧链接301重定向（正则表达式方式）
$HTTP["host"] == "www.xintuxiangce.top" {
    url.redirect = (
        "^/guide-(.+)\.html$" => "/guides/$1.html"
    )
}
```

**注意**：Lighttpd的url.redirect默认使用正则表达式，所以上面的配置应该可以工作。

### 方法三：创建独立的配置文件（推荐用于多站点）

如果使用虚拟主机配置，可以创建独立的配置文件：

**1. 创建重定向配置文件：**
```bash
cat > /etc/lighttpd/conf.d/guide-redirects.conf << 'EOF'
# 使用指南旧链接301重定向
$HTTP["host"] == "www.xintuxiangce.top" {
    url.redirect = (
        "^/guide-quick-start\.html$" => "/guides/quick-start.html",
        "^/guide-permissions\.html$" => "/guides/permissions.html",
        "^/guide-cleanup\.html$" => "/guides/cleanup.html",
        "^/guide-multidimensional-classification\.html$" => "/guides/multidimensional-classification.html"
    )
}
EOF
```

**2. 在主配置文件中包含此配置：**
```bash
# 编辑 /etc/lighttpd/lighttpd.conf
# 添加以下行（如果还没有）
include "conf.d/guide-redirects.conf"
```

## 📝 完整配置示例

如果你的Lighttpd配置文件结构如下，可以这样添加：

```lighttpd
# /etc/lighttpd/lighttpd.conf

# 服务器模块
server.modules = (
    "mod_access",
    "mod_alias",
    "mod_redirect",
    "mod_rewrite"
)

# 服务器配置
server.document-root = "/var/www/xintuxiangce/website"
server.port = 80
server.username = "lighttpd"
server.groupname = "lighttpd"

# 虚拟主机配置
$HTTP["host"] == "www.xintuxiangce.top" {
    server.document-root = "/var/www/xintuxiangce/website"
    
    # 使用指南旧链接301重定向
    url.redirect = (
        "^/guide-quick-start\.html$" => "/guides/quick-start.html",
        "^/guide-permissions\.html$" => "/guides/permissions.html",
        "^/guide-cleanup\.html$" => "/guides/cleanup.html",
        "^/guide-multidimensional-classification\.html$" => "/guides/multidimensional-classification.html"
    )
}
```

## ✅ 配置步骤

### 1. 备份配置文件

```bash
# 备份当前配置
cp /etc/lighttpd/lighttpd.conf /etc/lighttpd/lighttpd.conf.backup.$(date +%Y%m%d)
```

### 2. 编辑配置文件

```bash
# 使用vi或nano编辑
vi /etc/lighttpd/lighttpd.conf

# 或者
nano /etc/lighttpd/lighttpd.conf
```

### 3. 添加重定向规则

在配置文件的适当位置（通常在虚拟主机配置块内）添加重定向规则。

### 4. 测试配置

```bash
# 测试配置文件语法
lighttpd -t -f /etc/lighttpd/lighttpd.conf
```

如果显示 `Syntax OK`，说明配置正确。

### 5. 重启Lighttpd服务

```bash
# 重启服务
systemctl restart lighttpd

# 或者
service lighttpd restart

# 检查服务状态
systemctl status lighttpd
```

### 6. 验证重定向

```bash
# 测试重定向（应该返回301状态码）
curl -I http://www.xintuxiangce.top/guide-quick-start.html

# 应该看到类似输出：
# HTTP/1.1 301 Moved Permanently
# Location: /guides/quick-start.html
```

## 🔍 验证方法

### 方法1：使用curl命令

```bash
# 测试每个旧URL
curl -I http://www.xintuxiangce.top/guide-quick-start.html
curl -I http://www.xintuxiangce.top/guide-permissions.html
curl -I http://www.xintuxiangce.top/guide-cleanup.html
curl -I http://www.xintuxiangce.top/guide-multidimensional-classification.html
```

每个命令应该返回：
```
HTTP/1.1 301 Moved Permanently
Location: /guides/xxx.html
```

### 方法2：在浏览器中测试

1. 访问旧URL：`http://www.xintuxiangce.top/guide-quick-start.html`
2. 应该自动跳转到：`http://www.xintuxiangce.top/guides/quick-start.html`
3. 检查浏览器地址栏，确认URL已变更

### 方法3：使用在线工具

使用在线HTTP头检查工具：
- https://httpstatus.io/
- https://redirect-checker.org/

输入旧URL，检查是否返回301重定向。

## ⚠️ 注意事项

### 1. 确保mod_redirect模块已启用

检查配置文件中是否包含：
```lighttpd
server.modules += ( "mod_redirect" )
```

如果没有，需要添加。

### 2. 配置顺序很重要

重定向规则应该放在其他URL处理规则之前，确保优先匹配。

### 3. 正则表达式转义

在Lighttpd配置中，`.`需要转义为`\.`，`$`表示行尾。

### 4. 虚拟主机匹配

确保重定向规则在正确的虚拟主机配置块内（`$HTTP["host"] == "www.xintuxiangce.top"`）。

## 🐛 故障排查

### 问题1：重定向不工作

**检查：**
```bash
# 1. 检查配置语法
lighttpd -t -f /etc/lighttpd/lighttpd.conf

# 2. 检查错误日志
tail -f /var/log/lighttpd/error.log

# 3. 确认mod_redirect模块已加载
grep "mod_redirect" /etc/lighttpd/lighttpd.conf
```

### 问题2：返回404而不是301

**可能原因：**
- 重定向规则没有正确匹配
- 配置位置不对
- 虚拟主机配置不匹配

**解决：**
- 检查正则表达式是否正确
- 确认配置在正确的虚拟主机块内
- 检查Lighttpd版本是否支持该语法

### 问题3：重定向到错误的位置

**检查：**
- 确认目标URL路径正确
- 检查是否有其他重定向规则冲突

## 📋 完整配置示例（包含HTTPS）

如果你的网站同时支持HTTP和HTTPS，需要分别配置：

```lighttpd
# HTTP虚拟主机
$HTTP["host"] == "www.xintuxiangce.top" {
    server.document-root = "/var/www/xintuxiangce/website"
    
    # 使用指南旧链接301重定向
    url.redirect = (
        "^/guide-quick-start\.html$" => "/guides/quick-start.html",
        "^/guide-permissions\.html$" => "/guides/permissions.html",
        "^/guide-cleanup\.html$" => "/guides/cleanup.html",
        "^/guide-multidimensional-classification\.html$" => "/guides/multidimensional-classification.html"
    )
}

# HTTPS虚拟主机（如果使用SSL）
$SERVER["socket"] == ":443" {
    ssl.engine = "enable"
    ssl.pemfile = "/path/to/cert.pem"
    
    $HTTP["host"] == "www.xintuxiangce.top" {
        server.document-root = "/var/www/xintuxiangce/website"
        
        # 使用指南旧链接301重定向（HTTPS）
        url.redirect = (
            "^/guide-quick-start\.html$" => "/guides/quick-start.html",
            "^/guide-permissions\.html$" => "/guides/permissions.html",
            "^/guide-cleanup\.html$" => "/guides/cleanup.html",
            "^/guide-multidimensional-classification\.html$" => "/guides/multidimensional-classification.html"
        )
    }
}
```

## 🎯 推荐配置（最简洁）

**推荐使用正则表达式方式，一条规则匹配所有：**

```lighttpd
# 在虚拟主机配置块内添加
$HTTP["host"] == "www.xintuxiangce.top" {
    url.redirect = (
        "^/guide-(.+)\.html$" => "/guides/$1.html"
    )
}
```

这条规则会自动匹配所有 `/guide-*.html` 格式的URL，并重定向到 `/guides/*.html`。

## ✅ 配置检查清单

- [ ] 备份了原始配置文件
- [ ] 添加了重定向规则
- [ ] 确认mod_redirect模块已启用
- [ ] 测试配置语法：`lighttpd -t -f /etc/lighttpd/lighttpd.conf`
- [ ] 重启Lighttpd服务
- [ ] 使用curl测试每个旧URL返回301
- [ ] 在浏览器中测试重定向
- [ ] 检查错误日志确认没有错误

---

**配置完成后，搜索引擎会在下次抓取时发现301重定向，并自动更新索引。**

