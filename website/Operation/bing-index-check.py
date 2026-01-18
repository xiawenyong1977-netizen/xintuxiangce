#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bing 索引状态检查工具
检查网站技术配置，确保没有阻止 Bing 索引的问题
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse

BASE_URL = 'https://www.xintuxiangce.top'
SITEMAP_FILE = 'sitemap.xml'
ROBOTS_FILE = 'robots.txt'

def check_robots_txt():
    """检查 robots.txt"""
    print("\n" + "="*60)
    print("1. 检查 robots.txt")
    print("="*60)
    
    if not os.path.exists(ROBOTS_FILE):
        print("❌ robots.txt 文件不存在")
        return False
    
    with open(ROBOTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 检查是否阻止了 bingbot
    # 检查是否有明确的 Disallow: / 规则（这会阻止所有访问）
    if re.search(r'User-agent:\s*\*\s*\n\s*Disallow:\s*/\s*\n', content, re.MULTILINE):
        issues.append("❌ robots.txt 阻止了所有爬虫（Disallow: /）")
    elif re.search(r'User-agent:\s*bingbot\s*\n\s*Disallow:\s*/\s*\n', content, re.MULTILINE | re.IGNORECASE):
        issues.append("❌ robots.txt 明确阻止了 bingbot")
    else:
        print("✅ robots.txt 允许 bingbot 访问")
    
    # 检查是否有 sitemap 声明
    if 'Sitemap:' in content:
        print("✅ robots.txt 包含 sitemap 声明")
    else:
        issues.append("⚠️ robots.txt 缺少 sitemap 声明")
    
    if issues:
        for issue in issues:
            print(issue)
        return False
    
    return True

def check_meta_tags(file_path):
    """检查页面的 meta 标签"""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 检查 noindex
    if re.search(r'<meta\s+name=["\']robots["\'].*?noindex', content, re.IGNORECASE):
        issues.append("❌ 页面包含 noindex 标签")
    
    # 检查 canonical
    if '<link rel="canonical"' not in content:
        issues.append("⚠️ 页面缺少 canonical 标签")
    
    return issues if issues else None

def check_sitemap():
    """检查 sitemap.xml"""
    print("\n" + "="*60)
    print("2. 检查 sitemap.xml")
    print("="*60)
    
    if not os.path.exists(SITEMAP_FILE):
        print("❌ sitemap.xml 文件不存在")
        return False
    
    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计 URL 数量
    urls = re.findall(r'<ns0:loc>(.*?)</ns0:loc>', content)
    print(f"✅ sitemap.xml 包含 {len(urls)} 个 URL")
    
    # 检查主要页面
    important_pages = [
        BASE_URL + '/',
        BASE_URL + '/guides.html',
        BASE_URL + '/faq.html',
        BASE_URL + '/diary.html',
    ]
    
    missing = []
    for page in important_pages:
        if page not in urls:
            missing.append(page)
    
    if missing:
        print(f"⚠️ sitemap.xml 缺少以下重要页面:")
        for page in missing:
            print(f"   - {page}")
    else:
        print("✅ 所有重要页面都在 sitemap.xml 中")
    
    return True

def check_main_pages():
    """检查主要页面的 meta 标签"""
    print("\n" + "="*60)
    print("3. 检查主要页面的 Meta 标签")
    print("="*60)
    
    pages_to_check = [
        'index.html',
        'guides.html',
        'faq.html',
        'diary.html',
    ]
    
    all_ok = True
    for page in pages_to_check:
        if os.path.exists(page):
            issues = check_meta_tags(page)
            if issues:
                print(f"\n❌ {page}:")
                for issue in issues:
                    print(f"   {issue}")
                all_ok = False
            else:
                print(f"✅ {page}: Meta 标签正常")
        else:
            print(f"⚠️ {page}: 文件不存在")
    
    return all_ok

def generate_checklist():
    """生成 Bing Webmaster Tools 检查清单"""
    print("\n" + "="*60)
    print("4. Bing Webmaster Tools 检查清单")
    print("="*60)
    
    checklist = """
请在 Bing Webmaster Tools 中执行以下检查：

【检查 1: site: 搜索结果】
1. 在 Bing 搜索框中输入: site:www.xintuxiangce.top
2. 查看返回的搜索结果数量
   ✅ 如果返回很多结果 → 索引正常
   ❌ 如果返回很少或为空 → 索引问题

【检查 2: 索引覆盖报告】
1. 登录 Bing Webmaster Tools
2. 导航到: 索引 → 索引覆盖
3. 查看以下指标:
   - 已索引页面数量
   - "Excluded by policy"（政策排除）
   - "Low quality content"（低质量内容）
   - "Discovered but not crawled"（已发现但未抓取）
   - "Crawl errors"（抓取错误）

【检查 3: URL 检查工具】
1. 在 Bing Webmaster Tools 中使用 "URL 检查工具"
2. 测试以下页面:
   - https://www.xintuxiangce.top/
   - https://www.xintuxiangce.top/guides.html
   - https://www.xintuxiangce.top/faq.html
3. 确认每个页面:
   ✅ 页面可以抓取
   ✅ 页面可以索引
   ✅ 没有被 robots 或 meta 阻止

【检查 4: 站点地图状态】
1. 导航到: 站点地图
2. 检查 sitemap.xml 的状态:
   ✅ 已提交
   ✅ 状态正常
   ✅ 最近有更新

【检查 5: 抓取统计】
1. 导航到: 抓取统计
2. 查看 bingbot 的抓取情况:
   ✅ 最近有抓取活动
   ✅ 没有大量错误

【检查 6: 安全与手动操作】
1. 导航到: 安全与手动操作
2. 检查是否有:
   ❌ 手动操作（Manual Actions）
   ❌ 安全问题（Security Issues）
"""
    
    print(checklist)
    
    # 保存到文件
    with open('Operation/BING_CHECKLIST.md', 'w', encoding='utf-8') as f:
        f.write(f"# Bing Webmaster Tools 检查清单\n\n")
        f.write(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(checklist)
    
    print("\n✅ 检查清单已保存到: Operation/BING_CHECKLIST.md")

def main():
    print("="*60)
    print("Bing 索引状态检查工具")
    print("="*60)
    
    # 切换到 website 目录
    if os.path.basename(os.getcwd()) != 'website':
        if os.path.exists('website'):
            os.chdir('website')
    
    # 执行检查
    results = []
    results.append(("robots.txt", check_robots_txt()))
    results.append(("sitemap.xml", check_sitemap()))
    results.append(("主要页面 Meta 标签", check_main_pages()))
    
    # 生成检查清单
    generate_checklist()
    
    # 总结
    print("\n" + "="*60)
    print("检查总结")
    print("="*60)
    
    all_ok = True
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if not result:
            all_ok = False
    
    if all_ok:
        print("\n✅ 所有技术检查通过！")
        print("请按照检查清单在 Bing Webmaster Tools 中进行进一步检查。")
    else:
        print("\n⚠️ 发现一些问题，请先修复后再进行 Bing Webmaster Tools 检查。")
    
    print("\n下一步:")
    print("1. 查看 Operation/BING_CHECKLIST.md 获取详细检查步骤")
    print("2. 在 Bing Webmaster Tools 中执行检查")
    print("3. 根据检查结果采取相应措施")

if __name__ == '__main__':
    main()
