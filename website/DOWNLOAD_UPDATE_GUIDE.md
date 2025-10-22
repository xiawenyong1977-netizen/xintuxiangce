# 网站下载地址更新说明

## 更新内容

### 1. 目录结构变更
- **原路径**: `/var/www/dist/`
- **新路径**: 
  - 便携版: `/var/www/dist/pc/portable/`
  - 安装版: `/var/www/dist/pc/setup/`

### 2. 更新的文件

#### 2.1 JavaScript 文件
- **`script.js`**: 更新了文件检测逻辑，支持新的目录结构
- **`download-api.js`**: 添加了两种版本的文件列表支持

#### 2.2 HTML 文件
- **`index.html`**: 添加了"下载软件"链接
- **`download.html`**: 更新了文件检测路径
- **`download-select.html`**: 新增下载选择页面，支持便携版和安装版选择

#### 2.3 JSON 配置文件
- **`download-info.json`**: 添加了安装版配置，支持两种版本

#### 2.4 Python 脚本
- **`download.py`**: 更新了文件查找逻辑，优先查找便携版目录

### 3. 新功能

#### 3.1 版本选择页面
- 用户可以选择下载便携版或安装版
- 显示文件版本和大小信息
- 美观的界面设计

#### 3.2 智能文件检测
- 自动检测最新版本文件
- 支持多种文件名格式
- 回退机制确保兼容性

### 4. 文件命名规范

#### 4.1 便携版
- 格式: `xtxc{YYYYMMDDHHMM}.zip`
- 示例: `xtxc202510151254.zip`
- 路径: `dist/pc/portable/`

#### 4.2 安装版
- 格式: `xtxc{YYYYMMDDHHMM}-setup.exe`
- 示例: `xtxc202510151254-setup.exe`
- 路径: `dist/pc/setup/`

### 5. 部署说明

#### 5.1 服务器目录结构
```
/var/www/xintuxiangce/
├── dist/
│   └── pc/
│       ├── portable/
│       │   ├── xtxc202510151254.zip
│       │   └── xtxc202510111614.zip
│       └── setup/
│           ├── xtxc202510151254-setup.exe
│           └── xtxc202510111614-setup.exe
└── website/
    ├── index.html
    ├── download-select.html
    ├── download.html
    ├── script.js
    ├── download-api.js
    ├── download-info.json
    └── download.py
```

#### 5.2 权限设置
```bash
# 确保目录存在
sudo mkdir -p /var/www/xintuxiangce/dist/pc/portable
sudo mkdir -p /var/www/xintuxiangce/dist/pc/setup

# 设置权限
sudo chown -R www-data:www-data /var/www/xintuxiangce/dist/
sudo chmod -R 755 /var/www/xintuxiangce/dist/
```

### 6. 测试验证

#### 6.1 本地测试
- 启动本地服务器: `python -m http.server 8080`
- 访问: `http://localhost:8080/download-select.html`
- 测试两种版本的下载功能

#### 6.2 生产环境测试
- 确保文件路径正确
- 验证下载链接可访问
- 测试文件下载完整性

### 7. 注意事项

1. **向后兼容**: 保留了原有的文件检测逻辑作为回退方案
2. **文件大小**: 安装版通常比便携版稍大（约5MB差异）
3. **版本同步**: 确保便携版和安装版使用相同的版本号
4. **更新机制**: 新文件上传后，网站会自动检测最新版本

### 8. 后续优化建议

1. 添加文件校验和（MD5/SHA256）
2. 实现增量更新功能
3. 添加下载统计功能
4. 支持更多平台版本（Mac、Linux）
5. 实现自动更新检查机制
