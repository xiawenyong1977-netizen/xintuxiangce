# 芯图相册官网 - 官方网站源码

[![Website](https://img.shields.io/badge/website-https://www.xintuxiangce.top-blue.svg)](https://www.xintuxiangce.top/)
[![Software](https://img.shields.io/badge/software-芯图相册-green.svg)](https://www.xintuxiangce.top/#download)

## 📖 项目简介

**这是芯图相册的官方网站源码项目**，包含官网的HTML、CSS、JavaScript等前端代码。

**芯图相册**是一款基于AI技术的智能照片分类管理工具，帮助用户高效整理海量照片。本地处理，无需联网，90%+准确率自动识别分类照片，完全保护您的隐私安全。

> ⚠️ **注意**：本仓库只包含官网源码，不包含芯图相册软件的源代码。软件下载请访问官网。

**官网地址**: https://www.xintuxiangce.top/

## ✨ 核心特性

- 🤖 **AI智能识别**: 采用先进的深度学习技术，准确率高达90%以上
- 🔒 **隐私绝对安全**: 所有处理完全在本地进行，无需联网，零上传
- ⚡ **高效快速**: 优化的算法确保处理速度，大批量照片也能快速完成
- 🎯 **多维度分类**: 支持8大分类维度，包括按内容、城市、颜色、存储、格式、分辨率、方向、相似组分类
- ✏️ **灵活可控**: AI分类结果支持手动调整
- 🎨 **简洁易用**: 清晰直观的界面设计，简单四步即可完成照片整理

## 📦 项目结构

```
xintuxiangce-website/    # 官网源码项目
├── website/             # 官网源码
│   ├── index.html      # 主页面
│   ├── diary.html      # 芯图日记列表页
│   ├── diary/          # 芯图日记内容
│   │   ├── *.html      # 文章/视频详情页
│   │   ├── *.md        # Markdown源文件
│   │   └── article-template.html  # 详情页模板
│   ├── diary-data.json # 日记数据配置
│   ├── update-diary.py # 日记更新脚本
│   ├── blog.html       # 教程页面
│   ├── styles.css      # 样式文件
│   ├── script.js       # 交互脚本
│   ├── 404.html        # 404页面
│   ├── robots.txt      # SEO配置
│   ├── sitemap.xml     # 网站地图
│   └── *.md            # 文档文件
├── docs/               # 文档页面
├── icons/              # 应用图标
├── images/             # 应用截图
│   └── diary/          # 日记图片资源
├── *.html              # 搜索引擎验证文件
└── README.md          # 本文件
```

> 📝 **说明**：这是官网的前端源码，用于展示和推广芯图相册软件。软件本身是独立的Windows应用程序。

## 🚀 功能介绍

### 8大分类维度

芯图相册现在支持8大分类维度，让您从多个角度智能管理和查找照片：

#### 📷 按内容分类（AI分类）
使用AI大模型智能识别照片内容，支持9大内容类别：
- 📱 手机截图
- 🔲 二维码
- 🪪 证件照片
- 👤 单人照
- 👥 社交活动（多人照）
- 🏞️ 旅行风景
- 🍔 美食记录
- 🐱 宠物萌照
- 📷 其它

#### 🏙️ 按城市分类（本地算法）
根据照片EXIF信息中的GPS坐标，通过本地数据库自动匹配城市，按拍摄地点归类您的旅行回忆。

#### 🎨 按颜色分类（AI分类）
AI识别照片的主色调（背景颜色），按颜色主题分类，适合按风格整理照片。

#### 📁 按存储分类（本地算法）
根据照片的存储位置（文件夹路径）分类，方便按来源或项目管理照片。

#### 🖼️ 按格式分类（本地算法）
根据文件格式（JPEG、PNG、HEIC、WEBP等）自动分类，适合按技术需求管理照片。

#### 📐 按分辨率分类（本地算法）
智能识别照片分辨率（4K、1080p、720p等），按画质要求筛选照片。

#### 🔄 按方向分类（本地算法）
根据照片宽高比自动分类为横屏、竖屏、全景、正方形，适合按用途（壁纸、社交媒体）整理。

#### 🔗 相似组分类（本地算法）
使用颜色直方图、时间窗口、文本相似度等算法，智能识别重复或相似的照片，帮您快速清理，释放存储空间。

> **💡 平台支持**：所有多维度分类功能在**移动端（Android）**和**PC端（Windows）**都完全支持。

## 📥 下载

**Windows版本**: [下载地址](https://www.xintuxiangce.top/#download)

系统要求：
- Windows 10 或更高版本
- 4GB 以上内存（推荐8GB）
- 500MB 可用磁盘空间

## 🌐 在线体验

访问官网了解更多信息：https://www.xintuxiangce.top/

## 📝 使用指南

### 快速上手
1. **连接与设置**: 使用数据线连接手机与电脑，选定需要整理的相册目录
2. **一键智能分类**: 点击"开始智能分类"，AI将自动扫描识别
3. **便捷拣选暂存**: 分类完成后，勾选需要处理的照片，一键移入暂存箱
4. **最终清理或归档**: 进入暂存箱二次确认，删除或归档

### 📚 详细教程文章

我们提供了完整的使用指南，帮助您快速掌握芯图相册的各项功能：

- 📖 [**芯图相册使用指南：快速掌握PC端与移动端照片管理技巧**](https://www.xintuxiangce.top/guide-quick-start.html)
  - 从零开始，快速了解如何使用芯图相册进行智能照片分类和管理
  - 包含PC端（Windows）和移动端（Android）的完整操作步骤
  - 涵盖安装、设置、扫描、会员开通等详细说明

- 🔒 [**掌握芯图相册权限设置：保护隐私同时享受智能分类功能**](https://www.xintuxiangce.top/guide-permissions.html)
  - 详细说明Android版本需要哪些权限、这些权限的用途
  - 包含华为、小米、OPPO等各品牌手机的权限设置方法
  - 帮助您正确配置应用权限，保护隐私的同时享受智能分类功能

- 🚀 [**告别手动整理！芯图相册AI技术，7大分类助你高效清理照片**](https://www.xintuxiangce.top/guide-cleanup.html)
  - 详细说明如何使用AI智能分类功能快速清理手机照片
  - 包含7个智能分类介绍和完整的清理流程
  - 释放存储空间，让照片管理更高效

- 🎯 [**芯图相册多维度分类功能完整指南：8大分类维度助您高效管理照片**](https://www.xintuxiangce.top/guide-multidimensional-classification.html)
  - 详细介绍8大分类维度：按内容、按城市、按颜色、按存储、按格式、按分辨率、按方向、相似组分类
  - 包含AI分类和本地算法分类的详细说明
  - 支持移动端和PC端，帮助您从多个角度智能管理和查找照片

📋 [查看所有使用指南文章](https://www.xintuxiangce.top/guides.html)

## 🛠️ 技术栈

### 官网技术
- HTML5
- CSS3 (Flexbox, Grid, Animations)
- Vanilla JavaScript (ES6+)
- Lighttpd Web Server

### 特点
- 响应式设计，支持各种设备
- SEO优化，完整的TDK配置
- 无外部依赖，轻量高效
- 现代化UI设计

## 📊 性能指标

- 分类准确率: **90%+**
- 支持分类维度: **8大维度**
- 内容分类类别: **9大类**
- 测试数据: **1886张照片，8.86GB**
- 隐私保护: **100%本地处理**

## 🔒 隐私保护

- ✅ 本地AI处理，无需联网
- ✅ 不上传任何照片数据
- ✅ 不收集用户信息
- ✅ 无广告、无追踪
- ✅ 完全开放透明

## 📄 文档

### 用户使用文档
- 📖 [使用指南：快速掌握PC端与移动端照片管理技巧](https://www.xintuxiangce.top/guide-quick-start.html)
- 🔒 [权限设置说明：保护隐私同时享受智能分类功能](https://www.xintuxiangce.top/guide-permissions.html)
- 🚀 [快速清理指南：7大分类助你高效清理照片](https://www.xintuxiangce.top/guide-cleanup.html)
- 🎯 [多维度分类功能完整指南：8大分类维度助您高效管理照片](https://www.xintuxiangce.top/guide-multidimensional-classification.html)
- 📋 [所有使用指南文章](https://www.xintuxiangce.top/guides.html)

### 芯图日记
- 📝 [芯图日记](https://www.xintuxiangce.top/diary.html) - 大模型研发经验与产品运营分享
  - 分享大模型相关的研发经验、产品运营思路和技术实践
  - 包含文章和视频内容，每周更新
  - 涵盖AI协作、架构思维、学习路径等深度内容

### 开发文档
- [官网完整说明](website/README.md)
- [快速开始指南](website/QUICK_START.md)
- [部署指南](website/DEPLOYMENT.md)
- [HTTPS配置指南](website/HTTPS_SETUP_GUIDE.md)

## 🤝 贡献

欢迎提交问题和建议！

### 如何贡献
- 🐛 报告Bug：在[Issues](https://github.com/xiawenyong1977-netizen/xintuxiangce/issues)中提交问题
- 💡 功能建议：提出新功能想法
- 📝 文档改进：完善使用说明
- 🌟 给项目点星：支持项目发展

### 开发指南
```bash
# 克隆项目
git clone https://github.com/xiawenyong1977-netizen/xintuxiangce.git

# 进入项目目录
cd xintuxiangce

# 查看项目结构
ls -la
```

## 📚 相关资源

### 使用指南
- 📖 [使用指南列表](https://www.xintuxiangce.top/guides.html) - 完整的使用教程文章
- 🚀 [快速入门指南](https://www.xintuxiangce.top/guide-quick-start.html) - PC端与移动端照片管理技巧
- 🔒 [权限设置说明](https://www.xintuxiangce.top/guide-permissions.html) - 保护隐私同时享受智能分类
- 🧹 [快速清理指南](https://www.xintuxiangce.top/guide-cleanup.html) - 7大分类助你高效清理照片
- 🎯 [多维度分类功能指南](https://www.xintuxiangce.top/guide-multidimensional-classification.html) - 8大分类维度助您高效管理照片

### 芯图日记
- 📝 [芯图日记](https://www.xintuxiangce.top/diary.html) - 大模型研发经验与产品运营分享
  - 分享大模型相关的研发经验、产品运营思路和技术实践
  - 包含文章和视频内容，每周更新
  - 涵盖AI协作、架构思维、学习路径等深度内容

### 其他资源
- [技术博客](https://www.xintuxiangce.top/blog.html) - AI照片分类技术解析
- [常见问题](https://www.xintuxiangce.top/#faq) - FAQ解答
- [更新日志](https://github.com/xiawenyong1977-netizen/xintuxiangce/releases) - 版本更新记录

## 📮 联系方式

- 官网: https://www.xintuxiangce.top/


- GitHub: https://github.com/xiawenyong1977-netizen/xintuxiangce

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

感谢所有使用和支持芯图相册的用户！

---

**© 2025 芯图相册. 保留所有权利.**

*让照片管理更智能，让隐私更安全*

