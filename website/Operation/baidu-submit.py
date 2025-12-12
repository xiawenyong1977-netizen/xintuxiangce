#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度 URL 提交脚本
用于在页面更新后通知百度搜索引擎
"""

import requests
import sys
import os

# 百度提交配置
BAIDU_API_URL = "http://data.zz.baidu.com/urls"
SITE = "https://www.xintuxiangce.top"
TOKEN = "BkAC6dY605noLVUX"
BASE_URL = "https://www.xintuxiangce.top"

def submit_urls(urls):
    """
    提交 URL 到百度收录接口
    
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
            # 移除开头的斜杠，然后拼接
            clean_url = url.lstrip('/')
            full_urls.append(f"{BASE_URL}/{clean_url}")
    
    # 准备 URL 列表（每行一个）
    url_text = '\n'.join(full_urls)
    
    # 准备请求参数（注意：site 参数应该是域名，不带 https://）
    params = {
        "site": "www.xintuxiangce.top",  # 百度要求域名格式，不带协议
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
        
        # 百度 API 返回 JSON
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success', 0) > 0:
                    return f"✓ 百度收录: 成功提交 {result.get('success', 0)} 个 URL (剩余配额: {result.get('remain', 0)})"
                elif result.get('not_same_site'):
                    return f"✗ 百度收录: 错误 - URL 不属于该站点"
                elif result.get('not_valid'):
                    return f"✗ 百度收录: 错误 - URL 无效"
                else:
                    return f"✗ 百度收录: {result}"
            except:
                return f"✓ 百度收录: 成功 (HTTP {response.status_code}) - {response.text[:100]}"
        else:
            return f"✗ 百度收录: HTTP {response.status_code} - {response.text[:100]}"
    except Exception as e:
        return f"✗ 百度收录: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python baidu-submit.py <url1> [url2] [url3] ...")
        print("示例: python baidu-submit.py diary.html diary/video-001.html")
        sys.exit(1)
    
    urls = sys.argv[1:]
    print(f"提交 {len(urls)} 个 URL 到百度收录接口...")
    print(f"URLs: {', '.join(urls)}")
    print()
    
    result = submit_urls(urls)
    print(result)

