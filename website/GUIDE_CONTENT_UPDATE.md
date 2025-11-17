# 使用指南内容更新说明

## 文件结构

1. **guides.html** - 文章列表页面（中间页）
   - 显示所有使用指南文章的列表
   - 点击导航栏"使用指南"会跳转到这里

2. **guide-*.html** - 具体的文章详情页
   - 例如：`guide-quick-start.html` 是快速入门指南
   - 可以创建多个文章页面，如：`guide-advanced.html`、`guide-tips.html` 等

## 如何添加新文章

### 步骤1：创建文章详情页

复制 `guide-quick-start.html` 作为模板，创建新的文章页面，例如 `guide-advanced.html`：

```bash
cp guide-quick-start.html guide-advanced.html
```

### 步骤2：更新文章内容

打开新创建的文章文件，在 `<article class="article-body">` 标签内：

1. **替换标题**：修改 `<h1>` 标签中的标题
2. **添加文案**：将从公众号文章复制的文案粘贴到相应位置
3. **添加图片**：
   - 将公众号文章中的图片保存到 `/var/www/xintuxiangce/images/` 目录
   - 使用 `<img src="/images/图片文件名.jpg" alt="图片描述">` 插入图片

### 步骤3：更新文章列表

编辑 `guides.html`，在 JavaScript 的 `guides` 数组中添加新文章：

```javascript
const guides = [
    {
        id: 'quick-start',
        title: '快速入门指南',
        description: '从零开始，快速了解如何使用芯图相册...',
        image: '/assets/首页-1.jpg',
        readTime: '5分钟',
        url: 'guide-quick-start.html'
    },
    {
        id: 'advanced',
        title: '高级功能指南',  // 新文章
        description: '深入了解芯图相册的高级功能...',
        image: '/images/高级功能封面.jpg',
        readTime: '8分钟',
        url: 'guide-advanced.html'
    }
];
```

## 从公众号文章复制内容的步骤

### 1. 获取文章内容

- 在微信中打开公众号文章
- 复制文章中的所有文字内容
- 保存文章中的所有图片

### 2. 处理图片

1. 将图片保存到服务器：
   ```bash
   # 上传图片到服务器
   scp 图片文件名.jpg root@123.57.68.4:/var/www/xintuxiangce/images/
   ```

2. 设置图片权限：
   ```bash
   ssh root@123.57.68.4 "chown lighttpd:lighttpd /var/www/xintuxiangce/images/图片文件名.jpg && chmod 644 /var/www/xintuxiangce/images/图片文件名.jpg"
   ```

### 3. 编辑文章HTML

在文章详情页的 `<article class="article-body">` 中：

```html
<article class="article-body">
    <!-- 标题 -->
    <h2>文章标题</h2>
    
    <!-- 段落 -->
    <p>这里是段落文字内容...</p>
    
    <!-- 图片 -->
    <img src="/images/图片文件名.jpg" alt="图片描述">
    
    <!-- 列表 -->
    <ul>
        <li>列表项1</li>
        <li>列表项2</li>
    </ul>
    
    <!-- 子标题 -->
    <h3>子标题</h3>
    <p>更多内容...</p>
</article>
```

## HTML标签说明

- `<h2>` - 主标题（大标题）
- `<h3>` - 子标题（小标题）
- `<p>` - 段落文字
- `<ul>` / `<ol>` - 无序/有序列表
- `<li>` - 列表项
- `<img src="路径" alt="描述">` - 图片
- `<strong>` - 加粗文字
- `<em>` - 斜体文字

## 图片路径说明

- 如果图片在 `/var/www/xintuxiangce/images/` 目录，使用：`/images/图片名.jpg`
- 如果图片在 `/var/www/xintuxiangce/assets/` 目录，使用：`/assets/图片名.jpg`

## 部署更新

更新内容后，需要上传到服务器：

```bash
# 上传文章文件
scp guide-*.html root@123.57.68.4:/var/www/xintuxiangce/

# 上传图片
scp images/*.jpg root@123.57.68.4:/var/www/xintuxiangce/images/

# 设置权限
ssh root@123.57.68.4 "chown -R lighttpd:lighttpd /var/www/xintuxiangce/guide-*.html /var/www/xintuxiangce/images/ && chmod 644 /var/www/xintuxiangce/guide-*.html /var/www/xintuxiangce/images/*"
```

## 示例：完整的文章结构

```html
<article class="article-body">
    <h2>欢迎使用芯图相册</h2>
    <p>这里是开篇介绍文字...</p>
    
    <img src="/images/介绍图片.jpg" alt="产品介绍">
    
    <h2>第一步：连接设备</h2>
    <p>详细的操作说明...</p>
    
    <img src="/images/连接设备.jpg" alt="连接设备步骤">
    
    <h3>注意事项</h3>
    <ul>
        <li>注意项1</li>
        <li>注意项2</li>
    </ul>
    
    <h2>第二步：开始分类</h2>
    <p>更多内容...</p>
</article>
```

## 注意事项

1. **保持格式一致**：使用相同的HTML标签结构，保持页面风格统一
2. **图片优化**：上传前压缩图片，建议单张图片不超过500KB
3. **SEO优化**：确保每篇文章都有合适的标题和描述
4. **响应式设计**：图片会自动适应移动端，无需额外处理

## 快速检查清单

- [ ] 文章标题已更新
- [ ] 所有文案已复制并格式化
- [ ] 所有图片已上传到服务器
- [ ] 图片路径正确
- [ ] 文章已添加到列表页（guides.html）
- [ ] 文件权限已设置正确
- [ ] 在浏览器中测试显示正常

