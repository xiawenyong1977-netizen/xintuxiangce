#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用指南更新脚本
功能：
1. 读取 guides-data.json
2. 生成/更新指南列表页和详情页
3. 更新 sitemap.xml
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# 配置
GUIDES_DATA_FILE = 'guides-data.json'
GUIDES_DIR = 'guides'
TEMPLATE_DIR = 'guides'
SITEMAP_FILE = 'sitemap.xml'
BASE_URL = 'https://www.xintuxiangce.top'

def load_json(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 {e}")
        return None

def save_file(filepath, content):
    """保存文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ 已生成: {filepath}")

def format_date(date_str):
    """格式化日期"""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%Y年%m月%d日')
    except:
        return date_str

def escape_json_string(text):
    """
    转义JSON字符串中的特殊字符
    只转义JSON规范要求的特殊字符，中文引号等Unicode字符不需要转义
    """
    if not text:
        return ''
    
    # 将文本转换为字符串
    text = str(text)
    
    # 转义反斜杠（必须在其他转义之前）
    text = text.replace('\\', '\\\\')
    
    # 只转义英文双引号（中文引号是普通Unicode字符，不需要转义）
    text = text.replace('"', '\\"')
    
    # 转义其他JSON特殊字符
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    
    return text

def extract_existing_meta_description(html_file_path):
    """
    从现有HTML文件中提取meta description
    如果文件不存在或无法提取，返回None
    """
    if not os.path.exists(html_file_path):
        return None
    
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式提取meta description
        # 匹配 <meta name="description" content="...">
        match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
        
        return None
    except Exception as e:
        print(f"警告: 无法读取现有文件 {html_file_path}: {e}")
        return None

def generate_article_page(article, template_path, all_articles=None, output_path=None):
    """生成文章详情页"""
    # 读取模板
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"警告: 模板文件不存在 {template_path}")
        return None
    
    # 检查是否有手动调整的meta description
    description = article.get('description', '')
    if output_path:
        existing_description = extract_existing_meta_description(output_path)
        if existing_description and existing_description != description:
            # 如果现有文件的description与JSON中的不同，说明是手动调整过的，保留手动版本
            print(f"  检测到手动调整的meta description，保留现有版本（长度: {len(existing_description)}字符）")
            description = existing_description
    
    # 替换占位符
    replacements = {
        '{{TITLE}}': article.get('title', ''),
        '{{DESCRIPTION}}': description,  # 使用可能被手动调整过的description
        '{{TAGS}}': ', '.join(article.get('tags', [])),
        '{{COVER}}': article.get('cover', '/icons/imageclassify.png'),
        '{{ID}}': article.get('id', ''),
        '{{DATE}}': format_date(article.get('date', '')),
        '{{AUTHOR}}': article.get('author', '芯图团队'),
        '{{READTIME}}': article.get('readTime', article.get('duration', '')),
    }
    
    # 处理内容
    content = ''
    if article.get('type') == 'article':
        # 如果是文章，尝试读取Markdown文件
        content_file = article.get('content', '')
        if content_file and os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 移除第一个h1标题（因为header中已经有标题了）
                content = re.sub(r'^#\s+.*?\n', '', content, count=1, flags=re.MULTILINE)
                # 简单的Markdown到HTML转换（基础版）
                content = markdown_to_html(content)
        else:
            content = article.get('description', '')
    elif article.get('type') == 'video':
        # 视频页面特殊处理
        content = generate_video_content(article)
    
    replacements['{{CONTENT}}'] = content
    
    # 处理标签（需要同时处理开始和结束标记）
    tags = article.get('tags', [])
    if tags:
        tags_html = ''.join([f'<span class="article-tag">{tag}</span>' 
                            for tag in tags])
        # 替换条件块：{{#TAGS}}...{{/TAGS}} 替换为标签HTML
        # 需要保留div结构，替换注释位置，并移除标记
        def replace_tags(match):
            content = match.group(0)
            # 找到注释位置并替换
            content = content.replace('<!-- 标签会在这里自动生成 -->', tags_html)
            # 移除标记
            content = re.sub(r'\{\{#TAGS\}\}', '', content)
            content = re.sub(r'\{\{/TAGS\}\}', '', content)
            return content
        template = re.sub(r'\{\{#TAGS\}\}.*?\{\{/TAGS\}\}', replace_tags, template, flags=re.DOTALL)
    else:
        # 如果没有标签，移除整个条件块
        template = re.sub(r'\{\{#TAGS\}\}.*?\{\{/TAGS\}\}', '', template, flags=re.DOTALL)
    
    # 处理封面图片（需要同时处理开始和结束标记）
    if article.get('cover'):
        cover_html = f'<img src="{article["cover"]}" alt="{article["title"]}" class="article-cover">'
        # 替换条件块：{{#COVER}}...{{/COVER}} 替换为图片
        template = re.sub(r'\{\{#COVER\}\}.*?\{\{/COVER\}\}', cover_html, template, flags=re.DOTALL)
    else:
        # 如果没有封面，移除整个条件块
        template = re.sub(r'\{\{#COVER\}\}.*?\{\{/COVER\}\}', '', template, flags=re.DOTALL)
    
    # 处理相关文章
    related_ids = article.get('related', [])
    if related_ids and all_articles:
        # 创建ID到文章的映射
        articles_dict = {a.get('id'): a for a in all_articles}
        
        # 生成相关文章卡片
        related_items = []
        for related_id in related_ids:
            if related_id in articles_dict:
                related_article = articles_dict[related_id]
                related_items.append(f'''
                <a href="{related_id}.html" class="related-article-card">
                    <h3>{related_article.get('title', '')}</h3>
                    <p>{related_article.get('description', '')}</p>
                </a>''')
        
        if related_items:
            related_html = ''.join(related_items)
            # 替换条件块：{{#RELATED}}...{{RELATED_ITEMS}}...{{/RELATED}} 替换为相关文章HTML
            pattern = r'\{\{#RELATED\}\}(.*?)\{\{RELATED_ITEMS\}\}(.*?)\{\{/RELATED\}\}'
            def replace_related(match):
                before = match.group(1)
                after = match.group(2)
                return before + related_html + after
            template = re.sub(pattern, replace_related, template, flags=re.DOTALL)
            # 移除条件标记
            template = re.sub(r'\{\{#RELATED\}\}', '', template)
            template = re.sub(r'\{\{/RELATED\}\}', '', template)
        else:
            # 如果没有相关文章，移除整个条件块
            template = re.sub(r'\{\{#RELATED\}\}.*?\{\{/RELATED\}\}', '', template, flags=re.DOTALL)
    else:
        # 如果没有相关文章，移除整个条件块
        template = re.sub(r'\{\{#RELATED\}\}.*?\{\{/RELATED\}\}', '', template, flags=re.DOTALL)
    
    # 先处理JSON-LD中的占位符（需要转义）
    def replace_json_ld_placeholders(match):
        """替换JSON-LD脚本块中的占位符，并对字符串值进行转义"""
        json_content = match.group(1)
        
        # 转义标题和描述（这些会出现在JSON字符串值中）
        # JSON-LD中使用手动调整过的description（如果存在）
        escaped_title = escape_json_string(article.get('title', ''))
        escaped_description = escape_json_string(description)  # 使用可能被手动调整过的description
        
        # 替换占位符
        json_content = json_content.replace('{{TITLE}}', escaped_title)
        json_content = json_content.replace('{{DESCRIPTION}}', escaped_description)
        json_content = json_content.replace('{{COVER}}', article.get('cover', '/icons/imageclassify.png'))
        json_content = json_content.replace('{{DATE}}', format_date(article.get('date', '')))
        json_content = json_content.replace('{{ID}}', article.get('id', ''))
        
        return f'<script type="application/ld+json">\n    {json_content}\n    </script>'
    
    # 替换JSON-LD脚本块中的占位符
    html = re.sub(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
        replace_json_ld_placeholders,
        template,
        flags=re.DOTALL
    )
    
    # 执行其他替换（HTML属性中的占位符不需要转义，HTML会自动处理）
    for key, value in replacements.items():
        if key not in ['{{#COVER}}', '{{/COVER}}', '{{#TAGS}}', '{{/TAGS}}', '{{#RELATED}}', '{{/RELATED}}', '{{RELATED_ITEMS}}']:
            # HTML属性中的值需要转义HTML特殊字符
            if key in ['{{TITLE}}', '{{DESCRIPTION}}']:
                html_value = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
                html = html.replace(key, html_value)
            else:
                html = html.replace(key, str(value))
    
    return html

def generate_video_content(article):
    """生成视频页面内容"""
    video_url = article.get('videoUrl', '')
    platform = article.get('videoPlatform', 'bilibili')
    
    # 根据平台生成嵌入代码
    if platform == 'bilibili':
        bv_match = re.search(r'BV[\w]+', video_url)
        if bv_match:
            bv = bv_match.group()
            embed_code = f'''
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 20px 0;">
                <iframe src="//player.bilibili.com/player.html?bvid={bv}&page=1" 
                        scrolling="no" border="0" frameborder="no" framespacing="0" 
                        allowfullscreen="true" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
                </iframe>
            </div>
            '''
        else:
            embed_code = f'<p><a href="{video_url}" target="_blank">观看视频</a></p>'
    else:
        embed_code = f'<p><a href="{video_url}" target="_blank">观看视频</a></p>'
    
    content = f'''
    <div class="video-container">
        {embed_code}
        <h2>视频简介</h2>
        <p>{article.get('description', '')}</p>
    </div>
    '''
    
    if article.get('transcript'):
        content += f'''
        <h2>文字稿</h2>
        <div class="transcript">
            {article.get('transcript')}
        </div>
        '''
    
    return content

def markdown_to_html(markdown_text):
    """简单的Markdown到HTML转换（基础版）"""
    html = markdown_text
    
    # 先处理代码块（避免被其他规则误匹配）
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks)-1}__'
    html = re.sub(r'```(\w+)?\n(.*?)```', save_code_block, html, flags=re.DOTALL)
    
    # 粗体
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # 行内代码
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # 图片（必须在链接之前处理，因为图片语法类似但以!开头）
    def process_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        # 保持绝对路径不变，确保从网站根路径访问
        if not img_path.startswith('/') and not img_path.startswith('http'):
            img_path = '/' + img_path
        return f'__IMG_TAG__<img src="{img_path}" alt="{alt_text}" style="max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px;">__IMG_TAG__'
    
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', process_image, html)
    
    # 链接
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # 引用块
    def process_quote(match):
        return f'__QUOTE_TAG__<blockquote>{match.group(1)}</blockquote>__QUOTE_TAG__'
    html = re.sub(r'^> (.*)$', process_quote, html, flags=re.MULTILINE)
    
    # 标题（必须在列表之前处理）
    html = re.sub(r'^### (.*)$', r'__H3_TAG__<h3>\1</h3>__H3_TAG__', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)$', r'__H2_TAG__<h2>\1</h2>__H2_TAG__', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*)$', r'__H1_TAG__<h1>\1</h1>__H1_TAG__', html, flags=re.MULTILINE)
    
    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        parts = code_block.split('```')
        if len(parts) >= 3:
            code_content = parts[2] if len(parts) > 2 else parts[1] if len(parts) > 1 else ''
            html = html.replace(f'__CODE_BLOCK_{i}__', f'<pre><code>{code_content}</code></pre>')
        else:
            html = html.replace(f'__CODE_BLOCK_{i}__', f'<pre><code>{code_block}</code></pre>')
    
    # 列表和段落处理
    lines = html.split('\n')
    in_list = False
    result = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 跳过空行
        if not line_stripped:
            if in_list:
                result.append('</ul>')
                in_list = False
            continue
        
        # 处理列表项
        if line_stripped.startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            content = line_stripped[2:].strip()
            result.append(f'<li>{content}</li>')
        else:
            # 结束列表
            if in_list:
                result.append('</ul>')
                in_list = False
            
            # 检查是否是块级元素（已标记的）
            if '__H1_TAG__' in line or '__H2_TAG__' in line or '__H3_TAG__' in line:
                line = line.replace('__H1_TAG__', '').replace('__H2_TAG__', '').replace('__H3_TAG__', '')
                result.append(line)
            elif '__IMG_TAG__' in line:
                line = line.replace('__IMG_TAG__', '')
                result.append(line)
            elif '__QUOTE_TAG__' in line:
                line = line.replace('__QUOTE_TAG__', '')
                result.append(line)
            elif line_stripped.startswith('<pre>') or line_stripped.startswith('<blockquote>'):
                result.append(line)
            else:
                # 普通段落
                result.append(f'<p>{line_stripped}</p>')
    
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)

def update_sitemap(articles):
    """更新sitemap.xml"""
    sitemap_path = SITEMAP_FILE
    
    # 读取现有sitemap
    existing_urls = []
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
            existing_urls = re.findall(r'<loc>(.*?)</loc>', content)
    
    # 生成新的sitemap条目
    today = datetime.now().strftime('%Y-%m-%d')
    new_entries = []
    
    # 使用指南列表页
    new_entries.append(f'''    <url>
        <loc>{BASE_URL}/guides.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>''')
    
    # 每篇指南
    for article in articles:
        new_entries.append(f'''    <url>
        <loc>{BASE_URL}/guides/{article['id']}.html</loc>
        <lastmod>{article.get('date', today)}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>''')
    
    # 合并现有URL和新URL（去重）
    all_urls = set(existing_urls)
    for entry in new_entries:
        url_match = re.search(r'<loc>(.*?)</loc>', entry)
        if url_match:
            all_urls.add(url_match.group(1))
    
    # 生成完整sitemap（这里简化处理，实际应该保留原有结构）
    print(f"提示: 请手动更新 {sitemap_path} 添加使用指南相关URL")
    print("新增URL:")
    for entry in new_entries:
        print(entry)

def main():
    """主函数"""
    print("=" * 50)
    print("使用指南更新脚本")
    print("=" * 50)
    
    # 1. 加载数据
    print("\n1. 加载指南数据...")
    data = load_json(GUIDES_DATA_FILE)
    if not data:
        return
    
    articles = data.get('articles', [])
    print(f"   找到 {len(articles)} 篇指南")
    
    # 2. 确保目录存在
    os.makedirs(GUIDES_DIR, exist_ok=True)
    
    # 3. 生成详情页
    print("\n2. 生成详情页...")
    template_path = os.path.join(GUIDES_DIR, 'guide-template.html')
    
    for article in articles:
        article_id = article.get('id', '')
        if not article_id:
            continue
        
        output_path = os.path.join(GUIDES_DIR, f"{article_id}.html")
        html = generate_article_page(article, template_path, all_articles=articles, output_path=output_path)
        if html:
            save_file(output_path, html)
    
    # 4. 更新sitemap
    print("\n3. 更新sitemap...")
    update_sitemap(articles)
    
    print("\n" + "=" * 50)
    print("更新完成！")
    print("=" * 50)
    print("\n下一步:")
    print("1. 检查生成的HTML文件")
    print("2. 手动更新 sitemap.xml（或改进脚本自动更新）")
    print("3. 上传到服务器")
    print("4. 提交sitemap到搜索引擎")

if __name__ == '__main__':
    main()

