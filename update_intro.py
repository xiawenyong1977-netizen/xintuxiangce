#!/usr/bin/env python3
import re

# 读取文件
with open('/var/www/xintuxiangce/intro.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换下载链接
content = content.replace('href="download.py"', 'href="download-select.html"')

# 写回文件
with open('/var/www/xintuxiangce/intro.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('修改完成：下载链接已更新到版本选择页面')
