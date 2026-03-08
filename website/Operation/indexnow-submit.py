#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexNow API 提交工具
用于向 Bing 和 Yandex 即时通知页面更新

使用方法:
  python indexnow-submit.py              # 提交重要页面（5个）
  python indexnow-submit.py --all        # 提交所有页面（从 sitemap.xml 读取）
  python indexnow-submit.py --all --yes  # 自动提交所有页面（非交互模式）
  python indexnow-submit.py URL1 URL2 ...  # 仅提交指定的完整 URL（用于 meta 更新后通知 Bing）
  
参数说明:
  --all, -a    : 从 sitemap.xml 读取所有 URL 并提交
  --yes, -y    : 非交互模式，自动确认提交
  URL1 URL2... : 要提交的完整 URL（需以 https:// 开头），用于只通知部分页面更新
"""

import requests
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

BASE_URL = 'https://www.xintuxiangce.top'
INDEXNOW_API = 'https://api.indexnow.org/IndexNow'
SITEMAP_FILE = 'sitemap.xml'
MAX_BATCH_SIZE = 10000  # IndexNow API 建议每次不超过 10,000 个 URL

def get_indexnow_key():
    """获取 IndexNow 密钥"""
    # 检查网站根目录是否有 IndexNow 密钥文件
    # 从当前脚本所在目录开始查找
    script_dir = os.path.dirname(os.path.abspath(__file__))
    key_files = [
        os.path.join(script_dir, 'indexnow-key.txt'),
        'indexnow-key.txt',
        '.indexnow-key.txt',
        os.path.join(script_dir, '..', 'indexnow-key.txt'),
    ]
    
    for key_file in key_files:
        if os.path.exists(key_file):
            try:
                with open(key_file, 'r', encoding='utf-8') as f:
                    key = f.read().strip()
                    if key:
                        print(f"✅ 找到 IndexNow 密钥文件: {key_file}")
                        return key
            except Exception as e:
                print(f"⚠️ 读取密钥文件失败 {key_file}: {e}")
                continue
    
    # 如果没有找到，提示用户生成
    print("⚠️ 未找到 IndexNow 密钥文件")
    print("\n请按以下步骤生成密钥：")
    print("1. 登录 Bing Webmaster Tools")
    print("2. 导航到: 设置 → IndexNow")
    print("3. 生成密钥并下载密钥文件")
    print("4. 将密钥文件保存为: Operation/indexnow-key.txt")
    print("\n或者手动输入密钥（临时使用）:")
    return input("请输入 IndexNow 密钥（直接回车跳过）: ").strip()

def submit_urls(urls, key=None, batch_size=MAX_BATCH_SIZE):
    """提交 URL 到 IndexNow（支持批量提交）"""
    if not urls:
        print("❌ URL 列表为空")
        return False
    
    if not key:
        key = get_indexnow_key()
        if not key:
            print("❌ 未提供 IndexNow 密钥，跳过提交")
            return False
    
    # 提取域名（从第一个 URL）
    parsed = urlparse(urls[0] if urls else BASE_URL)
    host = parsed.netloc
    
    # 分批提交
    total_urls = len(urls)
    batches = [urls[i:i + batch_size] for i in range(0, total_urls, batch_size)]
    total_batches = len(batches)
    
    print(f"\n准备提交 {total_urls} 个 URL，分为 {total_batches} 批")
    print(f"API: {INDEXNOW_API}")
    print(f"Host: {host}")
    print(f"每批最多: {batch_size} 个 URL\n")
    
    success_count = 0
    fail_count = 0
    
    for i, batch in enumerate(batches, 1):
        print(f"[批次 {i}/{total_batches}] 正在提交 {len(batch)} 个 URL...")
        
        # 准备请求数据
        data = {
            "host": host,
            "key": key,
            "urlList": batch
        }
        
        try:
            response = requests.post(
                INDEXNOW_API,
                json=data,
                headers={
                    'Content-Type': 'application/json'
                },
                timeout=30  # 增加超时时间，因为批量提交可能需要更长时间
            )
            
            if response.status_code == 200:
                print(f"  ✅ 批次 {i} 提交成功（状态码: {response.status_code}）")
                success_count += len(batch)
            else:
                print(f"  ⚠️ 批次 {i} 提交失败（状态码: {response.status_code}）")
                print(f"     响应: {response.text[:200]}")
                fail_count += len(batch)
            
            # 批次之间稍作延迟，避免请求过快
            if i < total_batches:
                time.sleep(1)
                
        except Exception as e:
            print(f"  ❌ 批次 {i} 提交异常: {e}")
            fail_count += len(batch)
    
    # 总结
    print(f"\n提交完成:")
    print(f"  ✅ 成功: {success_count} 个 URL")
    if fail_count > 0:
        print(f"  ❌ 失败: {fail_count} 个 URL")
    
    return success_count > 0

def get_urls_from_sitemap(sitemap_path=None):
    """从 sitemap.xml 读取所有 URL"""
    if sitemap_path is None:
        # 尝试多个可能的路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(script_dir, '..', SITEMAP_FILE),
            SITEMAP_FILE,
            os.path.join('website', SITEMAP_FILE),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                sitemap_path = path
                break
    
    if not sitemap_path or not os.path.exists(sitemap_path):
        print(f"⚠️ 未找到 sitemap.xml 文件")
        return []
    
    try:
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取所有 <ns0:loc> 或 <loc> 标签中的 URL
        urls = re.findall(r'<(?:ns0:)?loc>(.*?)</(?:ns0:)?loc>', content)
        urls = [url.strip() for url in urls if url.strip()]
        
        print(f"✅ 从 {sitemap_path} 读取到 {len(urls)} 个 URL")
        return urls
    except Exception as e:
        print(f"❌ 读取 sitemap.xml 失败: {e}")
        return []

def get_important_urls():
    """获取需要提交的重要 URL"""
    urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/guides.html",
        f"{BASE_URL}/faq.html",
        f"{BASE_URL}/diary.html",
        f"{BASE_URL}/photobetter.html",
    ]
    return urls

def main():
    import sys
    
    print("=" * 60)
    print("IndexNow API 提交工具")
    print("=" * 60)
    print()
    print("此工具用于向 Bing 和 Yandex 即时通知页面更新")
    print("适用于解决 site: 搜索为空的问题")
    print()
    
    # 检查命令行参数
    use_all = '--all' in sys.argv or '-a' in sys.argv
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    # 从命令行提取以 https:// 开头的 URL（仅提交指定页面）
    arg_urls = [a for a in sys.argv[1:] if a.startswith('https://') and a not in ('--all', '-a', '--yes', '-y')]
    
    # 获取要提交的 URL
    if arg_urls:
        print("📋 模式: 仅提交命令行指定的 URL")
        urls = arg_urls
    elif use_all:
        print("📋 模式: 提交所有 URL（从 sitemap.xml 读取）")
        urls = get_urls_from_sitemap()
        if not urls:
            print("\n❌ 无法从 sitemap.xml 读取 URL，改用重要页面列表")
            urls = get_important_urls()
    else:
        print("📋 模式: 仅提交重要页面")
        urls = get_important_urls()
    
    if not urls:
        print("❌ 没有找到要提交的 URL")
        return
    
    print(f"\n准备提交 {len(urls)} 个页面")
    if len(urls) <= 10:
        print("URL 列表:")
        for url in urls:
            print(f"  - {url}")
    else:
        print("前 10 个 URL:")
        for url in urls[:10]:
            print(f"  - {url}")
        print(f"  ... 还有 {len(urls) - 10} 个 URL")
    
    # 确认
    if not auto_confirm:
        try:
            confirm = input(f"\n是否继续提交 {len(urls)} 个 URL？(y/n): ").strip().lower()
            if confirm != 'y':
                print("已取消")
                return
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️ 非交互模式，使用 --yes 参数可自动提交")
            return
    
    # 提交
    success = submit_urls(urls)
    
    if success:
        print("\n" + "=" * 60)
        print("提交完成！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 等待 1-3 天让 Bing 处理")
        print("2. 再次检查: site:www.xintuxiangce.top")
        print("3. 查看 Bing Webmaster Tools 中的索引统计")
        print("\n提示:")
        print("- IndexNow 提交后，Bing 会在 1-3 天内开始索引这些页面")
        print("- 如果使用 --all 参数，建议等待更长时间（1-2 周）")
    else:
        print("\n" + "=" * 60)
        print("提交失败")
        print("=" * 60)
        print("\n建议:")
        print("1. 检查网络连接")
        print("2. 确认 IndexNow 密钥正确")
        print("3. 使用 Bing Webmaster Tools 的 URL 检查工具手动提交")
        print("\n使用方法:")
        print("  python indexnow-submit.py          # 提交重要页面")
        print("  python indexnow-submit.py --all    # 提交所有页面（从 sitemap.xml）")
        print("  python indexnow-submit.py --all --yes  # 自动提交所有页面")

if __name__ == '__main__':
    main()
