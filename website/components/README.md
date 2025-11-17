# 公共组件系统使用说明

## 概述

这个组件系统用于统一管理网站的导航栏和底部栏，避免在多个页面中重复代码。当需要修改导航栏或底部栏时，只需修改组件文件即可，所有页面会自动更新。

## 文件结构

```
website/
├── components/
│   ├── navbar.html      # 导航栏组件
│   ├── footer.html      # 底部栏组件
│   └── README.md        # 本说明文件
├── components-loader.js # 组件加载器
└── [其他页面文件]
```

## 使用方法

### 1. 在页面中引入组件加载器

在 HTML 页面的 `<head>` 部分（在 `</head>` 之前）添加：

```html
<script src="components-loader.js"></script>
```

**注意：** 如果页面在子目录中（如 `diary/`），需要调整路径：

```html
<!-- 在 website/diary/ 目录下的页面 -->
<script src="../components-loader.js"></script>
```

### 2. 移除内联的导航栏和底部栏

从页面中删除原有的导航栏和底部栏 HTML 代码，组件加载器会自动插入。

**删除前：**
```html
<body>
    <nav class="navbar">
        <!-- 导航栏内容 -->
    </nav>
    
    <!-- 页面内容 -->
    
    <footer class="footer">
        <!-- 底部栏内容 -->
    </footer>
</body>
```

**删除后：**
```html
<body>
    <!-- 导航栏和底部栏将通过 components-loader.js 自动加载 -->
    
    <!-- 页面内容 -->
</body>
```

### 3. 修改组件

当需要修改导航栏或底部栏时：

1. **修改导航栏：** 编辑 `components/navbar.html`
2. **修改底部栏：** 编辑 `components/footer.html`

修改后，所有使用组件系统的页面都会自动更新。

## 路径处理

组件加载器会自动处理不同目录层级的路径问题：

- **根目录页面**（如 `index.html`）：使用 `components/navbar.html`
- **子目录页面**（如 `diary/article-001.html`）：自动使用 `../components/navbar.html`

组件中的相对路径（如图片、链接）也会根据页面位置自动调整。

## 注意事项

1. **组件加载器必须在 `</head>` 之前引入**，确保在页面加载时就能执行
2. **保持组件文件中的路径为相对路径**（相对于 `website` 目录），加载器会自动调整
3. **移动菜单功能**：组件加载器会自动初始化移动端菜单，无需额外代码
4. **如果页面有特殊的导航栏或底部栏需求**，可以保留内联代码，组件加载器不会覆盖已存在的元素

## 迁移现有页面

要将现有页面迁移到组件系统：

1. 在 `<head>` 中添加 `<script src="components-loader.js"></script>`
2. 删除页面中的 `<nav class="navbar">...</nav>` 部分
3. 删除页面中的 `<footer class="footer">...</footer>` 部分
4. 保存并测试页面

## 故障排除

如果组件没有加载：

1. 检查浏览器控制台是否有错误信息
2. 确认 `components-loader.js` 的路径正确
3. 确认 `components/` 目录存在且包含 `navbar.html` 和 `footer.html`
4. 检查网络请求，确认组件文件可以正常访问

