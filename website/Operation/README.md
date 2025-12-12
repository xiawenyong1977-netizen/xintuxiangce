# Operation 运营文档目录

本目录包含网站运营相关的所有文档和工具，包括知乎运营、外链获取策略、搜索引擎收录工具等。

## 📁 目录结构

### 知乎运营相关

#### 1. 知乎回答模板
- **知乎回答-手机照片太多怎么办.md** - 针对"手机照片太多怎么办？"问题的完整回答模板
- **知乎回答-照片管理软件推荐.md** - 针对"目前比较好用的照片管理软件有哪些？"问题的对比回答

#### 2. 运营策略
- **知乎运营策略指南.md** - 知乎平台运营完整指南
  - 发布频率建议
  - 最佳发布时间
  - 内容类型分配
  - 避免被识别为营销号的方法
  - 月度内容规划模板

### 外链获取策略

- **外链获取策略.md** - 外链获取完整策略文档
  - 内容营销方案
  - 目录提交指南
  - 社区参与策略
  - 合作伙伴链接
  - 具体执行清单

- **外链最佳实践指南.md** - 外链使用最佳实践
  - 各平台外链规则对比
  - 超链接 vs 文本链接
  - SEO角度分析
  - 各平台具体操作指南

### 搜索引擎收录工具

#### Google 相关工具
- **google-submit.py** - Google Search Console URL 提交工具
- **google-check-indexed.py** - 检查页面是否已被 Google 索引
- **google-check-all-pages.py** - 批量检查所有页面索引状态
- **google-check-site-commands.py** - 检查站点命令执行情况
- **google-site-commands.txt** - Google 站点命令列表
- **google-submit-urls-only.txt** - 待提交的 URL 列表
- **google-index-report-*.txt** - 索引状态报告
- **gsc_api.json** - Google Search Console API 配置

#### Baidu 相关工具
- **baidu-submit.py** - 百度站长平台 URL 提交工具
- **baidu-auto-submit.py** - 百度自动提交工具（支持定时任务）
- **baidu-check-site-commands.py** - 检查百度站点命令
- **baidu-diagnosis.py** - 百度站点诊断工具
- **baidu-site-commands.txt** - 百度站点命令列表
- **baidu-submit-list.txt** - 百度提交列表
- **baidu-submit-log.txt** - 百度提交日志
- **baidu-submit-urls-only.txt** - 待提交的 URL 列表
- **baidu-after-icp.md** - ICP 备案后百度提交说明文档

#### Bing/IndexNow 相关工具
- **indexnow-submit.py** - IndexNow URL 提交工具（支持 Bing 和 Yandex）
- **indexnow-key.txt** - IndexNow API 密钥
- **BingSiteAuth.xml** - Bing 网站验证文件

### 七牛云CDN工具

- **qiniu-upload.py** - 七牛云文件上传工具
- **qiniu-config.json** - 七牛云配置文件
- **qiniu-config.json.example** - 七牛云配置示例文件
- **QINIU_CDN_SETUP.md** - 七牛云CDN设置完整文档
- **export-cert-for-qiniu.sh** - 导出证书用于七牛云

### SSL证书管理工具

- **request-download-cert.sh** - 申请和下载SSL证书脚本
- **renew-and-upload-cert.sh** - 续期并上传证书脚本
- **check-certificate.sh** - 检查证书状态脚本
- **export-cert-for-qiniu.sh** - 导出证书用于CDN（七牛云）

## 📋 文档说明

### 知乎回答模板使用

1. **直接复制使用**
   - 可以直接复制到知乎回答框
   - 根据具体问题适当调整内容
   - 保持超链接格式

2. **内容调整**
   - 根据问题微调开头和结尾
   - 保持核心内容不变
   - 确保外链自然融入

3. **发布建议**
   - 参考《知乎运营策略指南.md》中的发布频率
   - 选择最佳发布时间
   - 及时回复评论

### 运营策略使用

1. **制定计划**
   - 参考《知乎运营策略指南.md》制定月度计划
   - 参考《外链获取策略.md》制定外链获取计划

2. **执行跟踪**
   - 记录发布内容
   - 跟踪效果数据
   - 优化策略

3. **持续优化**
   - 根据数据调整策略
   - 更新内容模板
   - 扩展话题范围

## 🛠️ 工具使用说明

### Google 收录工具

**提交URL到Google：**
```bash
python google-submit.py
```

**检查页面索引状态：**
```bash
python google-check-indexed.py
```

**批量检查所有页面：**
```bash
python google-check-all-pages.py
```

**检查站点命令：**
```bash
python google-check-site-commands.py
```

### Baidu 收录工具

**提交URL到百度：**
```bash
python baidu-submit.py
```

**自动提交（定时任务）：**
```bash
python baidu-auto-submit.py
```

**站点诊断：**
```bash
python baidu-diagnosis.py
```

**检查站点命令：**
```bash
python baidu-check-site-commands.py
```

### Bing/IndexNow 工具

**提交URL到Bing和Yandex：**
```bash
python indexnow-submit.py <url1> <url2> ...
```

**示例：**
```bash
python indexnow-submit.py diary/ai-pair-tools.html diary/ai-prompt-library.html
```

### 七牛云CDN工具

**上传文件到七牛云：**
```bash
python qiniu-upload.py
```

**配置说明：**
- 配置文件：`qiniu-config.json`
- 参考示例：`qiniu-config.json.example`
- 详细设置：参考 `QINIU_CDN_SETUP.md`

### SSL证书管理工具

**申请和下载证书：**
```bash
bash request-download-cert.sh
```

**续期并上传证书：**
```bash
bash renew-and-upload-cert.sh
```

**检查证书状态：**
```bash
bash check-certificate.sh
```

**导出证书用于CDN：**
```bash
bash export-cert-for-qiniu.sh
```

**注意事项：**
- IndexNow 密钥保存在 `indexnow-key.txt`
- 支持批量提交多个 URL
- 同时提交到 Bing 和 Yandex

## 🎯 快速开始

### 第一步：阅读策略文档
1. 先阅读《知乎运营策略指南.md》了解发布频率和最佳实践
2. 阅读《外链获取策略.md》了解外链获取方案
3. 阅读《外链最佳实践指南.md》了解各平台规则

### 第二步：准备内容
1. 使用知乎回答模板准备回答
2. 根据策略指南调整内容
3. 确保外链格式正确

### 第三步：执行发布
1. 按照发布频率计划执行
2. 选择最佳发布时间
3. 及时互动回复

### 第四步：提交搜索引擎
1. 新内容发布后，使用相应工具提交到搜索引擎
2. 定期检查索引状态
3. 跟踪收录效果

## 📊 文件统计

- **Markdown文档：** 8个（运营策略、回答模板、说明文档、CDN设置）
- **Python脚本：** 10个（搜索引擎工具、CDN工具）
- **Shell脚本：** 4个（证书管理脚本）
- **配置文件：** 8个（命令列表、日志、密钥等）
- **JSON配置：** 2个（Google API、七牛云配置）
- **XML文件：** 1个（Bing验证文件）
- **总计：** 33个文件

## 📊 文档更新记录

- 2025-12-12：创建目录，整理运营相关文档
- 2025-12-12：添加搜索引擎收录工具（Google、Baidu、Bing）
- 包含知乎回答模板、运营策略、外链获取策略、搜索引擎工具等

## 💡 使用建议

1. **定期更新**：根据实际效果更新策略和模板
2. **数据跟踪**：记录发布效果，优化策略
3. **内容扩展**：根据新话题创建新的回答模板
4. **平台扩展**：可以扩展到其他平台（掘金、CSDN等）
5. **自动化**：使用定时任务自动提交新内容到搜索引擎

## ⚠️ 注意事项

1. **API密钥安全**：`gsc_api.json` 和 `indexnow-key.txt` 包含敏感信息，不要提交到公开仓库
2. **提交频率**：避免过于频繁提交，遵守各平台限制
3. **内容质量**：确保提交的内容有价值，避免垃圾内容
4. **定期检查**：定期检查索引状态，及时发现问题
