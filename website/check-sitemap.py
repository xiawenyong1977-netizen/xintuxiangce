#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 sitemap.xml 是否包含所有网站链接
"""

import re
import os
from pathlib import Path
from xml.etree import ElementTree as ET

BASE_URL = 'https://www.xintuxiangce.top'
SITEMAP_FILE = 'sitemap.xml'

def get_sitemap_urls():
    """从 sitemap.xml 中提取所有 URL"""
    if not os.path.exists(SITEMAP_FILE):
        print(f"错误: sitemap文件不存在 {SITEMAP_FILE}")
        return set()
    
    urls = set()
    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式提取所有 <loc> 标签中的 URL
        for match in re.finditer(r'<loc>(.*?)</loc>', content):
            urls.add(match.group(1).strip())
    
    return urls

def get_website_html_files():
    """获取网站所有应该被索引的 HTML 文件"""
    html_files = set()
    
    # 根目录下的 HTML 文件
    root_dir = Path('.')
    for html_file in root_dir.glob('*.html'):
        if html_file.name == 'index.html':
            # index.html 对应首页
            html_files.add(f"{BASE_URL}/")
        else:
            html_files.add(f"{BASE_URL}/{html_file.name}")
    
    # guides 目录下的 HTML 文件（排除模板文件）
    guides_dir = Path('guides')
    if guides_dir.exists():
        for html_file in guides_dir.glob('*.html'):
            if html_file.name not in ['guide-template.html']:
                html_files.add(f"{BASE_URL}/guides/{html_file.name}")
    
    # diary 目录下的 HTML 文件（排除模板文件）
    diary_dir = Path('diary')
    if diary_dir.exists():
        for html_file in diary_dir.glob('*.html'):
            if html_file.name not in ['article-template.html']:
                html_files.add(f"{BASE_URL}/diary/{html_file.name}")
    
    return html_files

def main():
    print("=" * 60)
    print("Sitemap 完整性检查")
    print("=" * 60)
    print()
    
    # 获取 sitemap 中的 URL
    sitemap_urls = get_sitemap_urls()
    print(f"✓ Sitemap 中的 URL 数量: {len(sitemap_urls)}")
    
    # 获取网站所有 HTML 文件对应的 URL
    website_urls = get_website_html_files()
    print(f"✓ 网站 HTML 文件数量: {len(website_urls)}")
    print()
    
    # 找出缺失的 URL
    missing_urls = website_urls - sitemap_urls
    
    # 找出 sitemap 中多余的 URL（可能文件已删除）
    extra_urls = sitemap_urls - website_urls
    
    # 显示结果
    if missing_urls:
        print(f"⚠ 缺失的 URL ({len(missing_urls)} 个):")
        for url in sorted(missing_urls):
            print(f"  - {url}")
        print()
    else:
        print("✓ 所有网站页面都已包含在 sitemap 中")
        print()
    
    if extra_urls:
        print(f"ℹ Sitemap 中的额外 URL ({len(extra_urls)} 个，可能是已删除的文件或特殊页面):")
        for url in sorted(extra_urls):
            print(f"  - {url}")
        print()
    
    # 统计信息
    print("=" * 60)
    print("统计信息:")
    print(f"  Sitemap URL 总数: {len(sitemap_urls)}")
    print(f"  网站 HTML 文件总数: {len(website_urls)}")
    print(f"  缺失的 URL: {len(missing_urls)}")
    print(f"  额外的 URL: {len(extra_urls)}")
    print(f"  覆盖率: {((len(website_urls) - len(missing_urls)) / len(website_urls) * 100):.1f}%")
    print("=" * 60)
    
    # 按类别分类缺失的 URL
    if missing_urls:
        print("\n缺失 URL 分类:")
        root_missing = [url for url in missing_urls if url.count('/') == 2]
        guides_missing = [url for url in missing_urls if '/guides/' in url]
        diary_missing = [url for url in missing_urls if '/diary/' in url]
        
        if root_missing:
            print(f"  根目录页面 ({len(root_missing)} 个):")
            for url in sorted(root_missing):
                print(f"    - {url}")
        
        if guides_missing:
            print(f"  指南页面 ({len(guides_missing)} 个):")
            for url in sorted(guides_missing):
                print(f"    - {url}")
        
        if diary_missing:
            print(f"  日记页面 ({len(diary_missing)} 个):")
            for url in sorted(diary_missing):
                print(f"    - {url}")

if __name__ == '__main__':
    main()
