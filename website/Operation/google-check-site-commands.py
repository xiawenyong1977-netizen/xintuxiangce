#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 Google site: 搜索命令，用于手动检查页面收录状态
从 sitemap.xml 读取所有 URL，生成 site: 搜索命令
"""

import os
import sys
from xml.etree import ElementTree as ET

SITEMAP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitemap.xml")

def extract_urls_from_sitemap(sitemap_path):
    """从 sitemap.xml 提取所有 URL"""
    urls = []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # 处理命名空间
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url_elem in root.findall('ns:url', namespaces):
            loc_elem = url_elem.find('ns:loc', namespaces)
            if loc_elem is not None:
                url = loc_elem.text.strip()
                urls.append(url)
        
        return urls
    except Exception as e:
        print(f"⚠️  解析 sitemap.xml 失败: {e}")
        return []

def main():
    print("=" * 80)
    print("Google 收录状态检查 - site: 搜索命令生成器")
    print("=" * 80)
    print()
    
    if not os.path.exists(SITEMAP_FILE):
        print(f"⚠️  未找到 sitemap.xml 文件: {SITEMAP_FILE}")
        sys.exit(1)
    
    print(f"从 {SITEMAP_FILE} 读取 URL...")
    urls = extract_urls_from_sitemap(SITEMAP_FILE)
    
    if not urls:
        print("⚠️  未能从 sitemap.xml 提取到 URL")
        sys.exit(1)
    
    print(f"找到 {len(urls)} 个 URL")
    print()
    print("=" * 80)
    print("使用方法：")
    print("=" * 80)
    print("1. 复制下面的 site: 搜索命令")
    print("2. 在 Google 搜索框中逐个输入并搜索")
    print("3. 如果搜索结果中出现该页面，说明已被收录")
    print("4. 如果没有结果，说明尚未被收录")
    print()
    print("=" * 80)
    print("site: 搜索命令列表")
    print("=" * 80)
    print()
    
    for i, url in enumerate(urls, 1):
        # 提取路径部分（去掉域名）
        path = url.replace("https://www.xintuxiangce.top", "")
        if not path:
            path = "/"
        print(f"{i:2d}. site:{url}")
    
    print()
    print("=" * 80)
    print("批量检查建议：")
    print("=" * 80)
    print("1. 在 Google Search Console 中查看：")
    print("   https://search.google.com/search-console")
    print("   左侧菜单 -> '索引' -> '页面' -> 查看已索引的页面")
    print()
    print("2. 使用 URL 检查工具（Search Console）：")
    print("   左侧菜单 -> 'URL 检查' -> 输入 URL -> 查看索引状态")
    print()
    print("3. 使用 site: 搜索命令（适合少量页面）：")
    print("   在 Google 搜索框中输入 site:www.xintuxiangce.top")
    print("   可以查看所有已收录的页面")
    print()
    
    # 保存到文件
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "google-site-commands.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Google site: 搜索命令列表\n")
        f.write("=" * 80 + "\n")
        f.write(f"生成时间: {os.path.basename(__file__)}\n")
        f.write(f"总计: {len(urls)} 个页面\n\n")
        for i, url in enumerate(urls, 1):
            f.write(f"{i:2d}. site:{url}\n")
    
    print(f"命令列表已保存到: {output_file}")

if __name__ == "__main__":
    main()

