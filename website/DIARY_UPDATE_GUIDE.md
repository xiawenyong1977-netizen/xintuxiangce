# 芯图日记更新指南

## 快速开始

### 1. 添加新文章

**步骤：**

1. **创建Markdown文件**
   - 在 `diary/` 目录创建 `article-XXX.md` 文件
   - 使用Markdown格式编写内容

2. **更新 diary-data.json**
   ```json
   {
     "id": "article-002",
     "type": "article",
     "title": "文章标题",
     "description": "文章摘要（用于列表页和SEO）",
     "content": "diary/article-002.md",
     "author": "芯图团队",
     "date": "2025-01-27",
     "tags": ["标签1", "标签2"],
     "category": "研发经验",
     "cover": "../assets/diary/article-002-cover.jpg",
     "readTime": "10分钟",
     "related": []
   }
   ```

3. **添加封面图片**
   - 将封面图片保存到 `assets/diary/` 目录（注意：HTML中必须使用assets路径，因为assets是images的符号链接）
   - 建议尺寸：800x400px
   - 格式：JPG或PNG

4. **运行更新脚本**
   ```bash
   cd website
   python update-diary.py
   ```

5. **检查生成的文件**
   - 检查 `diary/article-002.html` 是否正确生成
   - 在浏览器中打开预览

### 2. 添加新视频

**步骤：**

1. **上传视频到视频平台**
   - 推荐：B站、YouTube、腾讯视频
   - 获取视频URL

2. **更新 diary-data.json**
   ```json
   {
     "id": "video-002",
     "type": "video",
     "title": "视频标题",
     "description": "视频描述",
     "videoUrl": "https://www.bilibili.com/video/BVxxxxx",
     "videoPlatform": "bilibili",
     "duration": "20:15",
     "transcript": "视频文字稿（可选，用于SEO）",
     "author": "芯图团队",
     "date": "2025-01-27",
     "tags": ["产品设计", "用户体验"],
     "category": "产品设计",
     "cover": "../assets/diary/video-002-cover.jpg",
     "related": []
   }
   ```

3. **添加封面图片**
   - 视频封面图片，建议尺寸：800x450px

4. **运行更新脚本**
   ```bash
   python update-diary.py
   ```

## 更新周期建议

### 每周更新一次

**时间安排：**
- **周一**：确定本周主题
- **周二-周四**：撰写/制作内容
- **周五**：审核和优化
- **周六**：发布和推广

**内容规划：**
- 第1周：产品设计思路
- 第2周：技术实现细节
- 第3周：用户体验优化
- 第4周：行业观察/案例分享

## SEO优化要点

### 每篇文章必须包含：

1. **标题优化**
   - 包含核心关键词
   - 长度：30-60字符
   - 吸引点击

2. **描述优化**
   - 150-160字符
   - 包含关键词
   - 吸引点击

3. **内容质量**
   - 至少1500字
   - 深度内容
   - 包含代码示例/图表

4. **内部链接**
   - 链接到产品页面
   - 链接到相关文章
   - 链接到使用指南

5. **图片优化**
   - 所有图片添加alt标签
   - 图片文件名包含关键词
   - 压缩图片大小

## 发布后工作

1. **更新sitemap.xml**
   - 手动添加新文章URL
   - 或改进脚本自动更新

2. **提交搜索引擎**
   - Google Search Console
   - 百度站长平台
   - Bing Webmaster Tools

3. **社交媒体推广**
   - 微信公众号
   - 技术社区（掘金、CSDN等）
   - 微博/Twitter

4. **监控数据**
   - 查看访问量
   - 分析用户行为
   - 优化内容策略

## 常见问题

### Q: 如何修改已发布的文章？
A: 修改Markdown文件或JSON数据，重新运行更新脚本即可。

### Q: 如何删除文章？
A: 从 `diary-data.json` 中删除对应条目，删除对应的HTML文件。

### Q: 如何修改文章模板？
A: 编辑 `diary/article-template.html`，然后重新运行脚本。

### Q: 支持哪些Markdown语法？
A: 当前脚本支持基础Markdown，如需更多功能，可以：
- 使用更强大的Markdown库（如marked.js）
- 在客户端渲染Markdown
- 使用静态站点生成器

## 进阶功能（可选）

### 1. RSS Feed
生成RSS feed，方便用户订阅。

### 2. 评论系统
集成第三方评论系统（如Gitalk、Valine）。

### 3. 搜索功能
添加全文搜索功能。

### 4. 标签云
展示所有标签，方便用户浏览。

### 5. 相关文章推荐
基于标签和分类推荐相关文章。

## 技术支持

如有问题，请查看：
- 设计方案文档：`DIARY_MODULE_DESIGN.md`
- 更新脚本：`update-diary.py`

