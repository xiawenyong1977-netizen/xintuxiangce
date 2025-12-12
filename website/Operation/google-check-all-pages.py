#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Search Console 全站收录状态检查脚本
从 sitemap.xml 读取所有 URL，批量检查收录状态
"""

import sys
import os
import re
import time
from datetime import datetime
from xml.etree import ElementTree as ET

# Google Search Console 配置
_script_dir = os.path.dirname(os.path.abspath(__file__))
_local_key = os.path.join(_script_dir, "gsc_api.json")
SERVICE_ACCOUNT_FILE = _local_key if os.path.exists(_local_key) else "/var/www/xintuxiangce/website/gsc_api.json"
SITE_URL = "https://www.xintuxiangce.top"
SITEMAP_FILE = os.path.join(_script_dir, "sitemap.xml")

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

def check_urls_indexed(urls):
    """
    检查 URL 是否被 Google 收录
    
    Args:
        urls: URL 列表
    """
    if not urls:
        print("⚠️  没有找到要检查的 URL")
        return
    
    # 检查是否有 API 密钥文件
    if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("⚠️  未找到 Google Search Console API 密钥文件")
        print(f"   预期路径: {SERVICE_ACCOUNT_FILE}")
        print()
        print("【使用替代方法检查收录状态】")
        print("在 Google 搜索框中输入以下命令逐个检查：")
        print("-" * 60)
        for url in urls:
            print(f'site:{url}')
        print("-" * 60)
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
        
        print("=" * 80)
        print("Google Search Console 全站收录状态检查")
        print("=" * 80)
        print()
        print(f"检查 {len(urls)} 个 URL 的收录状态...")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        results = []
        indexed_urls = []
        not_indexed_urls = []
        error_urls = []
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"[{i}/{len(urls)}] 检查: {url}", end=" ... ", flush=True)
                
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
                    indexed_urls.append(url)
                    status_text = "✓ 已收录"
                    if last_crawl_time:
                        try:
                            crawl_date = datetime.fromisoformat(last_crawl_time.replace('Z', '+00:00'))
                            status_text += f" (最后抓取: {crawl_date.strftime('%Y-%m-%d')})"
                        except:
                            pass
                    print(status_text)
                    results.append({
                        'url': url,
                        'status': 'indexed',
                        'verdict': verdict,
                        'last_crawl': last_crawl_time
                    })
                else:
                    not_indexed_urls.append(url)
                    print(f"✗ 未收录 (状态: {verdict})")
                    results.append({
                        'url': url,
                        'status': 'not_indexed',
                        'verdict': verdict,
                        'coverage_state': coverage_state
                    })
                
                # 添加延迟，避免触发速率限制（每秒最多2个请求）
                if i < len(urls):
                    time.sleep(0.5)
                
            except Exception as e:
                error_urls.append(url)
                error_msg = str(e)
                if 'timeout' in error_msg.lower() or 'Connection' in error_msg:
                    print("⚠️  网络超时")
                elif 'not found' in error_msg.lower() or 'permission' in error_msg.lower():
                    print("⚠️  权限问题")
                elif '403' in error_msg or 'Forbidden' in error_msg:
                    print("⚠️  权限不足")
                elif '429' in error_msg or 'rate limit' in error_msg.lower():
                    print("⚠️  速率限制，等待5秒...")
                    time.sleep(5)
                else:
                    print(f"✗ 错误: {error_msg[:50]}")
                
                results.append({
                    'url': url,
                    'status': 'error',
                    'error': error_msg[:100]
                })
                
                # 错误后也添加延迟
                if i < len(urls):
                    time.sleep(1)
        
        # 输出详细报告
        print()
        print("=" * 80)
        print("检查结果统计")
        print("=" * 80)
        print(f"总计: {len(urls)} 个页面")
        print(f"✓ 已收录: {len(indexed_urls)} 个 ({len(indexed_urls)/len(urls)*100:.1f}%)")
        print(f"✗ 未收录: {len(not_indexed_urls)} 个 ({len(not_indexed_urls)/len(urls)*100:.1f}%)")
        print(f"⚠️  检查失败: {len(error_urls)} 个 ({len(error_urls)/len(urls)*100:.1f}%)")
        print()
        
        # 详细列表
        if indexed_urls:
            print("=" * 80)
            print("✓ 已收录的页面:")
            print("=" * 80)
            for url in indexed_urls:
                print(f"  ✓ {url}")
            print()
        
        if not_indexed_urls:
            print("=" * 80)
            print("✗ 未收录的页面:")
            print("=" * 80)
            for url in not_indexed_urls:
                print(f"  ✗ {url}")
            print()
        
        if error_urls:
            print("=" * 80)
            print("⚠️  检查失败的页面:")
            print("=" * 80)
            for url in error_urls:
                print(f"  ⚠️  {url}")
            print()
        
        # 保存结果到文件
        report_file = os.path.join(_script_dir, f"google-index-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Google Search Console 收录状态检查报告\n")
            f.write("=" * 80 + "\n")
            f.write(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总计: {len(urls)} 个页面\n")
            f.write(f"已收录: {len(indexed_urls)} 个\n")
            f.write(f"未收录: {len(not_indexed_urls)} 个\n")
            f.write(f"检查失败: {len(error_urls)} 个\n\n")
            
            f.write("已收录的页面:\n")
            f.write("-" * 80 + "\n")
            for url in indexed_urls:
                f.write(f"{url}\n")
            f.write("\n")
            
            f.write("未收录的页面:\n")
            f.write("-" * 80 + "\n")
            for url in not_indexed_urls:
                f.write(f"{url}\n")
            f.write("\n")
            
            if error_urls:
                f.write("检查失败的页面:\n")
                f.write("-" * 80 + "\n")
                for url in error_urls:
                    f.write(f"{url}\n")
        
        print(f"详细报告已保存到: {report_file}")
        print()
        print("=" * 80)
        print("建议")
        print("=" * 80)
        if not_indexed_urls:
            print("对于未收录的页面，建议：")
            print("1. 在 Google Search Console 中手动提交 URL")
            print("2. 确保 sitemap.xml 已提交")
            print("3. 在社交媒体分享，获取外链")
            print("4. 优化内部链接结构，确保重要页面有链接指向")
        
    except ImportError:
        print("⚠️  需要安装 Google API 客户端库：")
        print("   pip install google-api-python-client google-auth")
    except Exception as e:
        print(f"⚠️  API 配置错误: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("Google Search Console 全站收录状态检查")
    print("=" * 80)
    print()
    
    # 从 sitemap.xml 提取 URL
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
    
    # 检查收录状态
    check_urls_indexed(urls)

