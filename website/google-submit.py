#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Search Console URL 提交脚本
用于在页面更新后通知 Google 搜索引擎

注意：使用此脚本需要先配置 Google Search Console API
配置步骤：
1. 访问 https://console.cloud.google.com
2. 创建项目并启用 Search Console API
3. 创建服务账号并下载 JSON 密钥文件
4. 在 Google Search Console 中添加服务账号为所有者
5. 将 JSON 密钥文件路径配置到 SERVICE_ACCOUNT_FILE 变量
"""

import requests
import json
import sys
import os
from datetime import datetime

# Google Search Console 配置
SERVICE_ACCOUNT_FILE = "/var/www/xintuxiangce/website/gsc_api.json"
SITE_URL = "https://www.xintuxiangce.top"

def submit_urls_manual(urls):
    """
    手动提交 URL 到 Google Search Console（通过 URL 检查工具）
    
    注意：Google 没有公开的批量提交 API，只能通过 Search Console 手动提交
    此函数提供提交说明和 URL 列表
    """
    if isinstance(urls, str):
        urls = [urls]
    
    # 确保 URL 是完整的
    full_urls = []
    for url in urls:
        if url.startswith('http'):
            full_urls.append(url)
        else:
            clean_url = url.lstrip('/')
            full_urls.append(f"{SITE_URL}/{clean_url}")
    
    print("=" * 60)
    print("Google Search Console 手动提交指南")
    print("=" * 60)
    print()
    print("Google 没有像 Bing IndexNow 那样的即时提交 API")
    print("需要通过 Google Search Console 手动提交")
    print()
    print("【提交步骤】")
    print("1. 访问: https://search.google.com/search-console")
    print("2. 选择您的网站属性")
    print("3. 点击左侧菜单 'URL 检查'")
    print("4. 输入要提交的 URL")
    print("5. 点击 '请求编入索引'")
    print()
    print("【待提交的 URL 列表】")
    print("-" * 60)
    for i, url in enumerate(full_urls, 1):
        print(f"{i}. {url}")
    print("-" * 60)
    print()
    print("【批量提交建议】")
    print("由于 Google 需要手动提交，建议：")
    print("1. 优先提交重要页面（首页、新页面）")
    print("2. 每天提交 10-20 个 URL（避免过度提交）")
    print("3. 确保 sitemap.xml 已提交（Google 会自动发现）")
    print()
    print("【加速收录的其他方法】")
    print("1. ✅ 已提交 sitemap.xml（最重要）")
    print("2. 在社交媒体分享，获取外链")
    print("3. 优化内部链接结构")
    print("4. 确保网站加载速度快")
    print("5. 定期更新内容")

def submit_via_api(urls):
    """
    通过 Google Search Console API 请求索引
    
    注意：Google Search Console API 没有批量提交 URL 的功能
    但可以通过 URL Inspection API 请求单个 URL 的索引
    """
    if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("⚠️  未找到服务账号文件，使用手动提交方式")
        return submit_urls_manual(urls)
    
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        # 加载服务账号凭据
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/webmasters']
        )
        
        # 创建 Search Console 服务
        service = build('searchconsole', 'v1', credentials=credentials)
        
        if isinstance(urls, str):
            urls = [urls]
        
        # 确保 URL 是完整的
        full_urls = []
        for url in urls:
            if url.startswith('http'):
                full_urls.append(url)
            else:
                clean_url = url.lstrip('/')
                full_urls.append(f"{SITE_URL}/{clean_url}")
        
        print("=" * 60)
        print("通过 Google Search Console API 请求索引")
        print("=" * 60)
        print()
        
        results = []
        success_count = 0
        
        for url in full_urls:
            try:
                # 注意：Google Search Console API 没有批量提交 URL 的功能
                # 只能通过 URL Inspection API 检查 URL 状态
                # 这会触发 Google 重新评估该 URL，但不是直接的"请求索引"
                request = service.urlInspection().index().inspect(
                    body={
                        'inspectionUrl': url,
                        'siteUrl': SITE_URL
                    }
                )
                response = request.execute()
                
                # 检查响应中的索引状态
                index_status = response.get('inspectionResult', {}).get('indexStatusResult', {})
                verdict = index_status.get('verdict', 'UNKNOWN')
                
                if verdict == 'PASS':
                    results.append(f"✓ {url}: 已检查，索引状态正常")
                else:
                    results.append(f"⚠️  {url}: 已检查，状态: {verdict}")
                success_count += 1
                
            except Exception as e:
                error_msg = str(e)
                if 'timeout' in error_msg.lower() or 'Connection' in error_msg:
                    results.append(f"⚠️  {url}: 网络超时，请稍后重试或使用手动提交")
                elif 'not found' in error_msg.lower() or 'permission' in error_msg.lower():
                    results.append(f"⚠️  {url}: 需要先在 Search Console 中验证网站")
                elif '403' in error_msg or 'Forbidden' in error_msg:
                    results.append(f"⚠️  {url}: 权限不足，请检查服务账号权限")
                else:
                    results.append(f"✗ {url}: {error_msg[:80]}")
        
        print("\n".join(results))
        print()
        print(f"成功检查: {success_count}/{len(full_urls)} 个 URL")
        print()
        print("【重要说明】")
        print("Google Search Console API 主要用于查询和检查 URL 状态")
        print("检查 URL 可以触发 Google 重新评估，但不是直接的批量提交")
        print()
        print("Google 主要通过以下方式发现和索引页面：")
        print("1. ✅ Sitemap.xml（最重要，已配置）")
        print("   - 在 Search Console 中提交: https://www.xintuxiangce.top/sitemap.xml")
        print("   - Google 会自动抓取 sitemap 中的新页面")
        print("2. 内部链接（网站内部链接）")
        print("   - 确保重要页面有内部链接指向")
        print("3. 外部链接（其他网站链接）")
        print("   - 在社交媒体分享，获取外链")
        print("4. 手动提交（通过 Search Console 网页界面）")
        print("   - 访问: https://search.google.com/search-console")
        print("   - 使用 'URL 检查' 工具手动提交")
        print()
        print("【加速收录的最佳方法】")
        print("✅ 确保 sitemap.xml 已在 Search Console 中提交（最重要）")
        print("✅ 在社交媒体分享新文章，获取外链")
        print("✅ 定期更新内容，保持网站活跃")
        print("✅ 优化内部链接结构，确保重要页面有链接指向")
        
    except ImportError:
        print("⚠️  需要安装 Google API 客户端库：")
        print("   pip install google-api-python-client google-auth")
        print()
        return submit_urls_manual(urls)
    except Exception as e:
        print(f"⚠️  API 配置错误: {e}")
        print()
        return submit_urls_manual(urls)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python google-submit.py <url1> [url2] [url3] ...")
        print("示例: python google-submit.py / diary.html")
        print()
        print("注意：Google 没有即时提交 API，此脚本提供手动提交指南")
        sys.exit(1)
    
    urls = sys.argv[1:]
    print(f"准备提交 {len(urls)} 个 URL 到 Google...")
    print()
    
    # 尝试使用 API 提交，如果失败则使用手动方式
    # 检查密钥文件是否存在
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        print("检测到 API 密钥文件，尝试使用 API 提交...")
        print()
        submit_via_api(urls)
    else:
        print("未找到 API 密钥文件，使用手动提交指南...")
        print()
        submit_urls_manual(urls)

