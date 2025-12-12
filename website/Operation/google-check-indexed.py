#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Search Console 收录状态检查脚本
用于检查哪些页面已被 Google 收录

注意：使用此脚本需要先配置 Google Search Console API
配置步骤：
1. 访问 https://console.cloud.google.com
2. 创建项目并启用 Search Console API
3. 创建服务账号并下载 JSON 密钥文件
4. 在 Google Search Console 中添加服务账号为所有者
5. 将 JSON 密钥文件路径配置到 SERVICE_ACCOUNT_FILE 变量
"""

import sys
import os
from datetime import datetime

# Google Search Console 配置
# 优先使用本地密钥文件，如果不存在则使用服务器路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_local_key = os.path.join(_script_dir, "gsc_api.json")
SERVICE_ACCOUNT_FILE = _local_key if os.path.exists(_local_key) else "/var/www/xintuxiangce/website/gsc_api.json"
SITE_URL = "https://www.xintuxiangce.top"

def check_urls_indexed(urls):
    """
    检查 URL 是否被 Google 收录
    
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
            clean_url = url.lstrip('/')
            full_urls.append(f"{SITE_URL}/{clean_url}")
    
    # 检查是否有 API 密钥文件
    if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("⚠️  未找到 Google Search Console API 密钥文件")
        print(f"   预期路径: {SERVICE_ACCOUNT_FILE}")
        print()
        print("【使用替代方法检查收录状态】")
        print("可以通过以下方式手动检查：")
        print()
        print("方法1: 使用 Google Search Console 网页界面")
        print("1. 访问: https://search.google.com/search-console")
        print("2. 选择您的网站属性")
        print("3. 点击左侧菜单 '索引' -> '页面'")
        print("4. 查看已索引的页面列表")
        print()
        print("方法2: 使用 site: 搜索命令")
        print("在 Google 搜索框中输入以下命令检查每个页面：")
        print("-" * 60)
        for url in full_urls:
            print(f'site:{url}')
        print("-" * 60)
        print()
        print("方法3: 使用 URL 检查工具")
        print("1. 访问: https://search.google.com/search-console")
        print("2. 使用 'URL 检查' 工具逐个检查")
        return
    
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
        
        print("=" * 60)
        print("Google Search Console 收录状态检查")
        print("=" * 60)
        print()
        print(f"检查 {len(full_urls)} 个 URL 的收录状态...")
        print()
        
        results = []
        indexed_count = 0
        not_indexed_count = 0
        error_count = 0
        
        for url in full_urls:
            try:
                # 使用 URL Inspection API 检查 URL 状态
                request = service.urlInspection().index().inspect(
                    body={
                        'inspectionUrl': url,
                        'siteUrl': SITE_URL
                    }
                )
                response = request.execute()
                
                # 解析响应
                inspection_result = response.get('inspectionResult', {})
                index_status = inspection_result.get('indexStatusResult', {})
                
                # 获取索引状态
                verdict = index_status.get('verdict', 'UNKNOWN')
                coverage_state = index_status.get('coverageState', 'UNKNOWN')
                last_crawl_time = index_status.get('lastCrawlTime', '')
                
                # 判断是否已收录
                is_indexed = verdict in ['PASS', 'PASS_WITH_WARNINGS'] or coverage_state == 'SUBMITTED_AND_INDEXED'
                
                if is_indexed:
                    indexed_count += 1
                    status_icon = "✓"
                    status_text = "已收录"
                    if last_crawl_time:
                        crawl_date = datetime.fromisoformat(last_crawl_time.replace('Z', '+00:00'))
                        status_text += f" (最后抓取: {crawl_date.strftime('%Y-%m-%d %H:%M')})"
                else:
                    not_indexed_count += 1
                    status_icon = "✗"
                    status_text = f"未收录 (状态: {verdict})"
                
                results.append(f"{status_icon} {url}")
                results.append(f"   {status_text}")
                
                # 如果有警告或错误，显示详细信息
                if verdict == 'PASS_WITH_WARNINGS':
                    page_fetch_state = index_status.get('pageFetchState', '')
                    if page_fetch_state:
                        results.append(f"   警告: {page_fetch_state}")
                elif verdict not in ['PASS', 'PASS_WITH_WARNINGS']:
                    results.append(f"   详细信息: {coverage_state}")
                
                results.append("")  # 空行分隔
                
            except Exception as e:
                error_count += 1
                error_msg = str(e)
                if 'timeout' in error_msg.lower() or 'Connection' in error_msg:
                    results.append(f"⚠️  {url}: 网络超时，请稍后重试")
                elif 'not found' in error_msg.lower() or 'permission' in error_msg.lower():
                    results.append(f"⚠️  {url}: 需要先在 Search Console 中验证网站")
                elif '403' in error_msg or 'Forbidden' in error_msg:
                    results.append(f"⚠️  {url}: 权限不足，请检查服务账号权限")
                else:
                    results.append(f"✗ {url}: {error_msg[:100]}")
                results.append("")
        
        # 输出结果
        print("\n".join(results))
        print()
        print("=" * 60)
        print("检查结果统计")
        print("=" * 60)
        print(f"已收录: {indexed_count} 个")
        print(f"未收录: {not_indexed_count} 个")
        print(f"检查失败: {error_count} 个")
        print(f"总计: {len(full_urls)} 个")
        print()
        
        if indexed_count > 0:
            print("✅ 已收录的页面可以正常在 Google 搜索结果中找到")
        if not_indexed_count > 0:
            print("⚠️  未收录的页面需要等待 Google 抓取，或通过以下方式加速：")
            print("   1. 在 Search Console 中手动提交 URL")
            print("   2. 确保 sitemap.xml 已提交")
            print("   3. 在社交媒体分享，获取外链")
        
    except ImportError:
        print("⚠️  需要安装 Google API 客户端库：")
        print("   pip install google-api-python-client google-auth")
        print()
        print("【使用替代方法检查收录状态】")
        print("在 Google 搜索框中输入以下命令：")
        print("-" * 60)
        for url in full_urls:
            print(f'site:{url}')
        print("-" * 60)
    except Exception as e:
        print(f"⚠️  API 配置错误: {e}")
        print()
        print("【使用替代方法检查收录状态】")
        print("在 Google 搜索框中输入以下命令：")
        print("-" * 60)
        for url in full_urls:
            print(f'site:{url}')
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python google-check-indexed.py <url1> [url2] [url3] ...")
        print("示例: python google-check-indexed.py / diary.html guide-multidimensional-classification.html")
        print()
        print("或者检查今天新增的4个页面：")
        print("python google-check-indexed.py guide-multidimensional-classification.html diary/ai-pair-program-intro.html diary/video-008.html diary/video-009.html")
        sys.exit(1)
    
    urls = sys.argv[1:]
    check_urls_indexed(urls)

