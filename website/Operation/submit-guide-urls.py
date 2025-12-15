#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提交使用指南新URL到搜索引擎
用于通知Google和Bing URL变更
"""

import sys
import os
import importlib.util

# 动态导入indexnow-submit.py
def import_module_from_file(filepath, module_name):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 导入IndexNow模块
indexnow_module = import_module_from_file(
    os.path.join(os.path.dirname(__file__), 'indexnow-submit.py'),
    'indexnow_submit'
)

# 导入百度提交模块
try:
    baidu_module = import_module_from_file(
        os.path.join(os.path.dirname(__file__), 'baidu-submit.py'),
        'baidu_submit'
    )
except:
    baidu_module = None

# 新URL列表
NEW_GUIDE_URLS = [
    "https://www.xintuxiangce.top/guides/quick-start.html",
    "https://www.xintuxiangce.top/guides/permissions.html",
    "https://www.xintuxiangce.top/guides/cleanup.html",
    "https://www.xintuxiangce.top/guides/multidimensional-classification.html",
    "https://www.xintuxiangce.top/guides/smart-classification.html",
    "https://www.xintuxiangce.top/guides/photo-formats.html",
    "https://www.xintuxiangce.top/guides/photo-classification-complete-guide.html",
    "https://www.xintuxiangce.top/guides/photo-classification-tools.html"
]

# 使用指南列表页
GUIDES_LIST_URL = "https://www.xintuxiangce.top/guides.html"

def main():
    """主函数"""
    print("=" * 60)
    print("提交使用指南新URL到搜索引擎")
    print("=" * 60)
    print()
    
    all_urls = [GUIDES_LIST_URL] + NEW_GUIDE_URLS
    
    print(f"准备提交 {len(all_urls)} 个URL:")
    for url in all_urls:
        print(f"  - {url}")
    print()
    
    # 1. 提交到IndexNow (Bing和Yandex)
    print("1. 提交到IndexNow (Bing/Yandex)...")
    try:
        results = indexnow_module.submit_urls(all_urls)
        for result in results:
            print(f"   {result}")
    except Exception as e:
        print(f"   ✗ IndexNow提交失败: {e}")
    print()
    
    # 2. 提交到百度
    if baidu_module:
        print("2. 提交到百度...")
        try:
            for url in all_urls:
                result = baidu_module.submit_urls(url)
                print(f"   {result}")
        except Exception as e:
            print(f"   ✗ 百度提交失败: {e}")
        print()
    else:
        print("2. 百度提交模块未找到，跳过")
        print()
    
    # 3. Google Search Console提示
    print("3. Google Search Console:")
    print("   请手动在Google Search Console中:")
    print("   - 提交更新的sitemap.xml")
    print("   - 使用URL检查工具请求索引新URL")
    print("   - 验证旧URL的301重定向")
    print()
    
    print("=" * 60)
    print("提交完成！")
    print("=" * 60)
    print()
    print("下一步:")
    print("1. 确认301重定向已配置")
    print("2. 在Google Search Console中提交更新的sitemap")
    print("3. 在Bing Webmaster Tools中提交更新的sitemap")
    print("4. 监控索引状态（1-2周内）")

if __name__ == "__main__":
    main()

