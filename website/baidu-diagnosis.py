#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度收录问题诊断脚本
分析可能导致百度不收录的原因
"""

import os
import sys
import requests
from xml.etree import ElementTree as ET

SITE_URL = "https://www.xintuxiangce.top"
SITEMAP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitemap.xml")
ROBOTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "robots.txt")

def check_robots_txt():
    """检查 robots.txt 是否阻止百度爬虫"""
    print("=" * 80)
    print("1. 检查 robots.txt")
    print("=" * 80)
    
    if not os.path.exists(ROBOTS_FILE):
        print("⚠️  robots.txt 文件不存在")
        return False
    
    with open(ROBOTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否禁止百度爬虫
    if 'User-agent: Baiduspider' in content or 'User-agent: *' in content:
        if 'Disallow: /' in content and 'Allow: /' not in content:
            print("❌ robots.txt 禁止了所有爬虫访问")
            return False
        elif 'Disallow: /' in content:
            print("⚠️  robots.txt 中有 Disallow 规则，请检查是否影响百度爬虫")
        else:
            print("✓ robots.txt 允许百度爬虫访问")
    
    # 检查是否有 sitemap
    if 'Sitemap:' in content:
        print("✓ robots.txt 中已声明 sitemap")
        sitemap_line = [line for line in content.split('\n') if 'Sitemap:' in line]
        for line in sitemap_line:
            print(f"  {line.strip()}")
    else:
        print("⚠️  robots.txt 中未声明 sitemap")
    
    return True

def check_sitemap():
    """检查 sitemap.xml"""
    print()
    print("=" * 80)
    print("2. 检查 sitemap.xml")
    print("=" * 80)
    
    if not os.path.exists(SITEMAP_FILE):
        print("❌ sitemap.xml 文件不存在")
        return False
    
    try:
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('ns:url', namespaces)
        
        print(f"✓ sitemap.xml 存在，包含 {len(urls)} 个 URL")
        
        # 检查是否可以访问
        try:
            response = requests.get(f"{SITE_URL}/sitemap.xml", timeout=10)
            if response.status_code == 200:
                print(f"✓ sitemap.xml 可以正常访问: {SITE_URL}/sitemap.xml")
            else:
                print(f"⚠️  sitemap.xml 访问异常: HTTP {response.status_code}")
        except Exception as e:
            print(f"⚠️  无法访问 sitemap.xml: {e}")
        
        return True
    except Exception as e:
        print(f"❌ sitemap.xml 解析失败: {e}")
        return False

def check_website_accessibility():
    """检查网站可访问性"""
    print()
    print("=" * 80)
    print("3. 检查网站可访问性")
    print("=" * 80)
    
    try:
        response = requests.get(SITE_URL, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
        })
        
        if response.status_code == 200:
            print(f"✓ 网站可以正常访问 (HTTP {response.status_code})")
            print(f"  响应大小: {len(response.content)} 字节")
            
            # 检查是否有明显的内容
            if len(response.content) < 1000:
                print("⚠️  响应内容较小，可能影响收录")
            
            return True
        else:
            print(f"❌ 网站访问异常: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 网站无法访问: {e}")
        return False

def check_baidu_submit_config():
    """检查百度提交配置"""
    print()
    print("=" * 80)
    print("4. 检查百度提交配置")
    print("=" * 80)
    
    submit_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baidu-submit.py")
    if not os.path.exists(submit_script):
        print("⚠️  百度提交脚本不存在")
        return False
    
    with open(submit_script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'TOKEN' in content:
        print("✓ 百度提交脚本存在，已配置 TOKEN")
    else:
        print("⚠️  百度提交脚本中未找到 TOKEN 配置")
    
    # 检查提交接口
    if 'data.zz.baidu.com' in content:
        print("✓ 百度提交接口配置正确")
    else:
        print("⚠️  百度提交接口配置可能有问题")
    
    return True

def generate_recommendations():
    """生成优化建议"""
    print()
    print("=" * 80)
    print("百度收录优化建议")
    print("=" * 80)
    print()
    
    recommendations = [
        {
            "title": "1. 百度站长平台验证和配置",
            "items": [
                "访问 https://ziyuan.baidu.com/ 注册并验证网站",
                "在 '数据引入' -> '链接提交' 中配置推送接口",
                "在 '数据引入' -> 'Sitemap' 中提交 sitemap.xml",
                "确保网站验证方式正确（推荐使用文件验证或HTML标签验证）"
            ]
        },
        {
            "title": "2. 定期提交 URL",
            "items": [
                "每天提交新页面到百度（使用 baidu-submit.py 脚本）",
                "百度每日推送配额：普通站点 10 个/天，优质站点更多",
                "优先提交重要页面（首页、新文章、新功能页面）",
                "建议在页面发布后立即提交"
            ]
        },
        {
            "title": "3. 内容质量优化",
            "items": [
                "确保页面内容原创、有价值",
                "保持内容更新频率（定期发布新内容）",
                "优化页面标题和描述（TDK）",
                "确保页面加载速度快（影响爬虫抓取）"
            ]
        },
        {
            "title": "4. 外链建设",
            "items": [
                "在社交媒体分享网站内容（微博、知乎、CSDN等）",
                "在其他网站发布文章并链接回本站",
                "参与相关社区讨论，适当分享网站链接",
                "注意：外链要自然，避免过度优化"
            ]
        },
        {
            "title": "5. 技术优化",
            "items": [
                "确保网站 HTTPS 正常（已配置）",
                "优化移动端体验（百度优先收录移动友好网站）",
                "确保网站结构清晰，导航合理",
                "使用语义化 HTML 标签"
            ]
        },
        {
            "title": "6. 耐心等待",
            "items": [
                "百度收录通常比 Google 慢，新站可能需要 1-3 个月",
                "持续更新内容和提交 URL",
                "定期在百度站长平台查看索引量和抓取情况",
                "如果 3 个月后仍无收录，检查是否有其他问题"
            ]
        },
        {
            "title": "7. 检查工具",
            "items": [
                "使用 site:www.xintuxiangce.top 在百度搜索检查",
                "在百度站长平台查看 '索引量' 和 '抓取诊断'",
                "使用 '链接提交' -> '提交历史' 查看提交状态",
                "检查 '抓取异常' 是否有错误提示"
            ]
        }
    ]
    
    for rec in recommendations:
        print(rec["title"])
        for item in rec["items"]:
            print(f"  • {item}")
        print()

def main():
    print("=" * 80)
    print("百度收录问题诊断")
    print("=" * 80)
    print()
    print(f"网站: {SITE_URL}")
    print()
    
    # 执行检查
    check_robots_txt()
    check_sitemap()
    check_website_accessibility()
    check_baidu_submit_config()
    
    # 生成建议
    generate_recommendations()
    
    print("=" * 80)
    print("诊断完成")
    print("=" * 80)
    print()
    print("【重要提示】")
    print("百度收录是一个长期过程，特别是新站。")
    print("建议：")
    print("1. 确保已在百度站长平台验证网站")
    print("2. 每天提交新页面（使用 baidu-submit.py）")
    print("3. 保持内容更新频率")
    print("4. 耐心等待 1-3 个月")

if __name__ == "__main__":
    main()

