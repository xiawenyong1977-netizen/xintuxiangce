# 组件系统迁移指南

## 快速迁移步骤

### 1. 根目录页面（如 index.html, faq.html 等）

**步骤：**

1. 在 `</head>` 之前添加：
   ```html
   <script src="components-loader.js"></script>
   ```

2. 删除整个 `<nav class="navbar">...</nav>` 块

3. 删除整个 `<footer class="footer">...</footer>` 块

4. 在 `<body>` 标签后添加注释（可选）：
   ```html
   <!-- 导航栏和底部栏将通过 components-loader.js 自动加载 -->
   ```

### 2. 子目录页面（如 diary/article-001.html）

**步骤：**

1. 在 `</head>` 之前添加：
   ```html
   <script src="../components-loader.js"></script>
   ```

2. 删除整个 `<nav class="navbar">...</nav>` 块

3. 删除整个 `<footer class="footer">...</footer>` 块

### 3. 更深层级的子目录（如 diary/subdir/page.html）

**步骤：**

1. 在 `</head>` 之前添加：
   ```html
   <script src="../../components-loader.js"></script>
   ```

2. 删除导航栏和底部栏代码

## 批量迁移脚本（可选）

如果需要批量迁移多个文件，可以使用以下 PowerShell 脚本：

```powershell
# 批量添加组件加载器到根目录页面
$files = Get-ChildItem -Path "website\*.html" -Exclude "index.html"
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -notmatch "components-loader.js") {
        $content = $content -replace "(</head>)", "    <script src=`"components-loader.js`"></script>`n$1"
        Set-Content $file.FullName -Value $content -NoNewline
        Write-Host "已更新: $($file.Name)"
    }
}
```

## 验证

迁移后，请验证：

1. ✅ 页面正常显示导航栏和底部栏
2. ✅ 导航链接可以正常跳转
3. ✅ 移动端菜单可以正常打开/关闭
4. ✅ 二维码图片正常显示
5. ✅ 所有链接路径正确

## 回滚

如果需要回滚到内联代码：

1. 从组件文件复制内容到页面
2. 删除 `<script src="components-loader.js"></script>`
3. 根据页面位置调整路径（如 `../icons/` 等）

