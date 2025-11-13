#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexNow URL 提交脚本
用于在页面更新后通知 Bing 和 Yandex 搜索引擎
"""

import requests
import json
import sys

# IndexNow 配置
INDEXNOW_KEY = "UYrGqVGXSQHBvPqdBoudcs1E76P3if5l"
INDEXNOW_ENDPOINTS = [
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow"
]
BASE_URL = "https://www.xintuxiangce.top"

def submit_urls(urls):
    """
    提交 URL 到 IndexNow
    
    Args:
        urls: URL 列表，可以是单个字符串或字符串列表
    """
    if isinstance(urls, str):
        urls = [urls]
    
    # 确保 URL 是完整的
    full_urls = []
    for url in urls:
        if url.startswith('http'):
            full_urls.append(url)
        else:
            full_urls.append(f"{BASE_URL}/{url.lstrip('/')}")
    
    # 准备请求数据
    data = {
        "host": "www.xintuxiangce.top",
        "key": INDEXNOW_KEY,
        "urlList": full_urls
    }
    
    results = []
    for endpoint in INDEXNOW_ENDPOINTS:
        try:
            response = requests.post(
                endpoint,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            # IndexNow API 返回 200 或 202 都表示成功
            if response.status_code in [200, 202]:
                results.append(f"✓ {endpoint}: 成功 (HTTP {response.status_code})")
            else:
                results.append(f"✗ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            results.append(f"✗ {endpoint}: {str(e)}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python indexnow-submit.py <url1> [url2] [url3] ...")
        print("示例: python indexnow-submit.py index.html photobetter.html")
        sys.exit(1)
    
    urls = sys.argv[1:]
    print(f"提交 {len(urls)} 个 URL 到 IndexNow...")
    print(f"URLs: {', '.join(urls)}")
    print()
    
    results = submit_urls(urls)
    for result in results:
        print(result)

