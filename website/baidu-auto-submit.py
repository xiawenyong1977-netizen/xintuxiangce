#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度自动提交脚本
从 sitemap.xml 读取所有 URL，自动提交到百度
建议每天运行一次，提交新页面
"""

import os
import sys
import requests
from xml.etree import ElementTree as ET
from datetime import datetime

# 百度提交配置
BAIDU_API_URL = "http://data.zz.baidu.com/urls"
SITE = "https://www.xintuxiangce.top"
TOKEN = "BkAC6dY605noLVUX"
BASE_URL = "https://www.xintuxiangce.top"

# 文件路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
SITEMAP_FILE = os.path.join(_script_dir, "sitemap.xml")
SUBMIT_LOG = os.path.join(_script_dir, "baidu-submit-log.txt")

def extract_urls_from_sitemap(sitemap_path):
    """从 sitemap.xml 提取所有 URL"""
    urls = []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
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

def load_submitted_urls():
    """加载已提交的 URL 列表（从日志文件）"""
    submitted = set()
    if os.path.exists(SUBMIT_LOG):
        try:
            with open(SUBMIT_LOG, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        # 格式：2025-12-05 10:00:00 | URL
                        parts = line.strip().split(' | ')
                        if len(parts) >= 2:
                            submitted.add(parts[1].strip())
        except:
            pass
    return submitted

def save_submit_log(urls, result):
    """保存提交日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(SUBMIT_LOG, 'a', encoding='utf-8') as f:
        f.write(f"\n# {timestamp} - 批量提交\n")
        for url in urls:
            f.write(f"{timestamp} | {url}\n")
        f.write(f"# 结果: {result}\n")

def submit_urls_to_baidu(urls):
    """提交 URL 到百度"""
    if not urls:
        return "没有要提交的 URL"
    
    # 准备 URL 列表（每行一个）
    url_text = '\n'.join(urls)
    
    # 准备请求参数
    params = {
        "site": "www.xintuxiangce.top",
        "token": TOKEN
    }
    
    try:
        response = requests.post(
            BAIDU_API_URL,
            params=params,
            data=url_text.encode('utf-8'),
            headers={"Content-Type": "text/plain"},
            timeout=10
        )
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success', 0) > 0:
                    return f"✓ 成功提交 {result.get('success', 0)} 个 URL (剩余配额: {result.get('remain', 0)})"
                elif result.get('not_same_site'):
                    return f"✗ 错误 - URL 不属于该站点"
                elif result.get('not_valid'):
                    return f"✗ 错误 - URL 无效"
                else:
                    return f"✗ {result}"
            except:
                return f"✓ 成功 (HTTP {response.status_code}) - {response.text[:100]}"
        else:
            return f"✗ HTTP {response.status_code} - {response.text[:100]}"
    except Exception as e:
        return f"✗ {str(e)}"

def main():
    print("=" * 80)
    print("百度自动提交脚本")
    print("=" * 80)
    print()
    
    # 检查参数
    force_all = '--all' in sys.argv or '-a' in sys.argv
    
    # 从 sitemap 读取 URL
    if not os.path.exists(SITEMAP_FILE):
        print(f"❌ 未找到 sitemap.xml: {SITEMAP_FILE}")
        sys.exit(1)
    
    print(f"从 {SITEMAP_FILE} 读取 URL...")
    all_urls = extract_urls_from_sitemap(SITEMAP_FILE)
    
    if not all_urls:
        print("❌ 未能从 sitemap.xml 提取到 URL")
        sys.exit(1)
    
    print(f"找到 {len(all_urls)} 个 URL")
    print()
    
    # 决定提交哪些 URL
    if force_all:
        urls_to_submit = all_urls
        print("模式: 提交所有 URL (--all)")
    else:
        # 只提交未提交过的 URL
        submitted_urls = load_submitted_urls()
        urls_to_submit = [url for url in all_urls if url not in submitted_urls]
        
        if not urls_to_submit:
            print("✓ 所有 URL 都已提交过")
            print("如需重新提交所有 URL，请使用: python baidu-auto-submit.py --all")
            return
        
        print(f"模式: 仅提交新 URL")
        print(f"已提交过: {len(submitted_urls)} 个")
        print(f"待提交: {len(urls_to_submit)} 个")
    
    print()
    print("=" * 80)
    print("提交 URL 列表")
    print("=" * 80)
    for i, url in enumerate(urls_to_submit, 1):
        print(f"{i:2d}. {url}")
    print()
    
    # 百度每日配额限制（普通站点 10 个/天）
    if len(urls_to_submit) > 10:
        print("⚠️  注意：百度普通站点每日推送配额为 10 个 URL")
        print(f"   您要提交 {len(urls_to_submit)} 个 URL，将分批提交")
        print()
        
        # 分批提交
        batches = [urls_to_submit[i:i+10] for i in range(0, len(urls_to_submit), 10)]
        for i, batch in enumerate(batches, 1):
            print(f"提交第 {i}/{len(batches)} 批 ({len(batch)} 个 URL)...")
            result = submit_urls_to_baidu(batch)
            print(result)
            save_submit_log(batch, result)
            if i < len(batches):
                print("等待 1 秒后继续...")
                import time
                time.sleep(1)
    else:
        # 一次性提交
        print(f"提交 {len(urls_to_submit)} 个 URL 到百度...")
        result = submit_urls_to_baidu(urls_to_submit)
        print(result)
        save_submit_log(urls_to_submit, result)
    
    print()
    print("=" * 80)
    print("提交完成")
    print("=" * 80)
    print()
    print("【重要提示】")
    print("1. 百度收录需要时间，通常需要 1-3 个月")
    print("2. 建议每天运行此脚本一次，提交新页面")
    print("3. 在百度站长平台查看提交状态：https://ziyuan.baidu.com/")
    print("4. 使用 site:www.xintuxiangce.top 在百度搜索检查收录情况")

if __name__ == "__main__":
    main()

