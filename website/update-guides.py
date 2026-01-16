#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用指南更新脚本
功能：
1. 读取 guides-data.json
2. 生成/更新指南列表页和详情页
3. 更新 sitemap.xml

使用方法：
   全量生成：python update-guides.py
   只生成新增：python update-guides.py --incremental
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

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
    
    # 先处理表格（必须在其他规则之前，避免被误处理）
    def process_table(match):
        table_content = match.group(0)
        lines = [line.strip() for line in table_content.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return table_content
        
        # 处理每一行，移除引用块前缀
        processed_lines = []
        for line in lines:
            # 移除引用块前缀 > 
            if line.startswith('> '):
                line = line[2:].strip()
            processed_lines.append(line)
        
        # 第一行是表头
        header_line = processed_lines[0]
        # 第二行是分隔符，跳过
        # 从第三行开始是数据行
        
        # 提取表头单元格（Markdown表格格式：| col1 | col2 |，分割后第一个和最后一个可能是空字符串）
        header_cells = [cell.strip() for cell in header_line.split('|')]
        # 过滤掉空字符串
        header_cells = [cell for cell in header_cells if cell]
        
        if not header_cells:
            return table_content
        
        # 生成表头HTML
        header_html = '<thead><tr style="background-color: #f2f2f2;">' + ''.join([f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>' for cell in header_cells]) + '</tr></thead>'
        
        # 生成表体HTML
        body_html = '<tbody>'
        for line in processed_lines[2:]:  # 跳过表头和分隔符
            # 提取单元格（Markdown表格格式：| col1 | col2 |，分割后第一个和最后一个可能是空字符串）
            cells = [cell.strip() for cell in line.split('|')]
            # 过滤掉空字符串
            cells = [cell for cell in cells if cell]
            if cells:
                # 如果列数不匹配，补齐或截断
                while len(cells) < len(header_cells):
                    cells.append('')
                cells = cells[:len(header_cells)]
                body_html += '<tr>' + ''.join([f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>' for cell in cells]) + '</tr>'
        body_html += '</tbody>'
        
        return f'__TABLE_TAG__<table style="border-collapse: collapse; width: 100%; margin: 20px 0; border: 1px solid #ddd;">{header_html}{body_html}</table>__TABLE_TAG__'
    
    # 匹配表格：以 | 开头和结尾的行，至少3行（表头、分隔符、至少一行数据）
    # 支持引用块内的表格（每行可能以 > 开头）
    html = re.sub(r'(?:^> )?\|.+\|\s*\n(?:^> )?\|[:\-| ]+\|\s*\n(?:(?:^> )?\|.+\|\s*\n?)+', process_table, html, flags=re.MULTILINE)
    
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
    
    # 引用块（需要排除表格行）
    def process_quote(match):
        content = match.group(1)
        # 如果这行是表格的一部分，不处理
        if content.strip().startswith('|') and '|' in content:
            return match.group(0)
        return f'__QUOTE_TAG__<blockquote>{content}</blockquote>__QUOTE_TAG__'
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
    
    # 处理表格（必须在段落处理之前）
    def process_table_block(lines, start_idx):
        """处理表格块，返回(表格HTML, 结束索引)"""
        if start_idx >= len(lines):
            return None, start_idx
        
        # 检查是否是表格行（以 | 开头和结尾）
        table_lines = []
        i = start_idx
        in_quote = False
        
        while i < len(lines):
            line = lines[i]
            original_line = line
            line_stripped = line.strip()
            
            # 检查是否在引用块中
            if line_stripped.startswith('> '):
                in_quote = True
                # 移除 > 前缀和后面的空格
                line_content = line_stripped[2:].strip()
            else:
                in_quote = False
                line_content = line_stripped
            
            # 检查是否是表格行（必须以 | 开头）
            if line_content.startswith('|') and line_content.count('|') >= 2:
                table_lines.append((line_content, in_quote))
                i += 1
            elif i == start_idx:
                # 第一行不是表格，直接返回
                return None, start_idx
            else:
                # 遇到非表格行，停止
                break
        
        if len(table_lines) < 2:  # 至少需要表头和分隔符
            return None, start_idx
        
        # 解析表格
        header_line, header_in_quote = table_lines[0]
        separator_line, _ = table_lines[1] if len(table_lines) > 1 else ('', False)
        data_lines = [line for line, _ in table_lines[2:]] if len(table_lines) > 2 else []
        
        # 提取表头单元格（Markdown表格格式：| col1 | col2 |，分割后第一个和最后一个可能是空字符串）
        header_cells = [cell.strip() for cell in header_line.split('|')]
        # 过滤掉空字符串
        header_cells = [cell for cell in header_cells if cell]
        
        if not header_cells:
            return None, start_idx
        
        # 生成表头HTML
        header_html = '<thead><tr style="background-color: #f2f2f2;">' + ''.join([f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{cell}</th>' for cell in header_cells]) + '</tr></thead>'
        
        # 生成表体HTML
        body_html = '<tbody>'
        for data_line_tuple in table_lines[2:]:
            data_line, in_quote = data_line_tuple
            # 提取单元格（Markdown表格格式：| col1 | col2 |，分割后第一个和最后一个可能是空字符串）
            cells = [cell.strip() for cell in data_line.split('|')]
            # 过滤掉空字符串
            cells = [cell for cell in cells if cell]
            if cells:
                # 如果列数不匹配，补齐或截断
                while len(cells) < len(header_cells):
                    cells.append('')
                cells = cells[:len(header_cells)]
                body_html += '<tr>' + ''.join([f'<td style="border: 1px solid #ddd; padding: 8px;">{cell}</td>' for cell in cells]) + '</tr>'
        body_html += '</tbody>'
        
        table_html = f'<table style="border-collapse: collapse; width: 100%; margin: 20px 0; border: 1px solid #ddd;">{header_html}{body_html}</table>'
        return table_html, i
    
    # 列表和段落处理
    lines = html.split('\n')
    in_list = False
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # 跳过空行
        if not line_stripped:
            if in_list:
                result.append('</ul>')
                in_list = False
            i += 1
            continue
        
        # 检查是否是表格
        table_html, table_end_idx = process_table_block(lines, i)
        if table_html:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(table_html)
            i = table_end_idx
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
            elif '__TABLE_TAG__' in line:
                line = line.replace('__TABLE_TAG__', '')
                result.append(line)
            elif line_stripped.startswith('<pre>') or line_stripped.startswith('<blockquote>') or line_stripped.startswith('<table>'):
                result.append(line)
            elif line_stripped.startswith('|') and '|' in line_stripped:
                # 可能是表格行，但没被正确识别，跳过（避免重复处理）
                pass
            else:
                # 普通段落
                result.append(f'<p>{line_stripped}</p>')
        
        i += 1
    
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)

def update_sitemap(articles, incremental=False):
    """更新sitemap.xml"""
    sitemap_path = SITEMAP_FILE
    
    if not os.path.exists(sitemap_path):
        print(f"错误: sitemap文件不存在 {sitemap_path}")
        return False
    
    try:
        # 读取现有sitemap内容
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        # 解析现有sitemap
        root = ET.fromstring(sitemap_content)
        
        # 获取命名空间（如果有）
        ns = {}
        if root.tag.startswith('{'):
            ns_uri = root.tag[1:].split('}')[0]
            ns['sitemap'] = ns_uri
            ns_prefix = '{' + ns_uri + '}'
        else:
            ns_prefix = ''
        
        # 获取现有的URL列表
        existing_urls = {}
        for url_elem in root.findall(f'.//{ns_prefix}url'):
            loc_elem = url_elem.find(f'{ns_prefix}loc')
            if loc_elem is not None:
                url = loc_elem.text.strip()
                lastmod_elem = url_elem.find(f'{ns_prefix}lastmod')
                lastmod = lastmod_elem.text.strip() if lastmod_elem is not None else None
                existing_urls[url] = {'elem': url_elem, 'lastmod': lastmod}
        
        # 生成需要添加的URL
        today = datetime.now().strftime('%Y-%m-%d')
        guides_list_url = f"{BASE_URL}/guides.html"
        new_urls = []
        updated_count = 0
        
        # 检查并添加使用指南列表页
        if guides_list_url not in existing_urls:
            url_elem = ET.SubElement(root, f'{ns_prefix}url')
            ET.SubElement(url_elem, f'{ns_prefix}loc').text = guides_list_url
            ET.SubElement(url_elem, f'{ns_prefix}lastmod').text = today
            ET.SubElement(url_elem, f'{ns_prefix}changefreq').text = 'weekly'
            ET.SubElement(url_elem, f'{ns_prefix}priority').text = '0.9'
            new_urls.append(guides_list_url)
            updated_count += 1
        
        # 添加每篇指南
        for article in articles:
            article_url = f"{BASE_URL}/guides/{article['id']}.html"
            article_date = article.get('date', today)
            
            # 检查URL是否已存在
            if article_url in existing_urls:
                # 如果已存在，更新lastmod（如果不是增量模式）
                if not incremental:
                    url_info = existing_urls[article_url]
                    lastmod_elem = url_info['elem'].find(f'{ns_prefix}lastmod')
                    if lastmod_elem is not None:
                        if lastmod_elem.text != article_date:
                            lastmod_elem.text = article_date
                            updated_count += 1
                    else:
                        ET.SubElement(url_info['elem'], f'{ns_prefix}lastmod').text = article_date
                        updated_count += 1
                continue
            
            # 添加新的URL条目
            url_elem = ET.SubElement(root, f'{ns_prefix}url')
            ET.SubElement(url_elem, f'{ns_prefix}loc').text = article_url
            ET.SubElement(url_elem, f'{ns_prefix}lastmod').text = article_date
            ET.SubElement(url_elem, f'{ns_prefix}changefreq').text = 'monthly'
            ET.SubElement(url_elem, f'{ns_prefix}priority').text = '0.8'
            new_urls.append(article_url)
            updated_count += 1
        
        if new_urls or updated_count > 0:
            # 保存更新后的sitemap
            # 使用 minidom 格式化输出
            from xml.dom import minidom
            xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')
            dom = minidom.parseString(xml_str)
            formatted_xml = dom.toprettyxml(indent="    ", encoding='utf-8').decode('utf-8')
            
            # 移除 XML 声明后的空行
            lines = formatted_xml.split('\n')
            if lines[0].startswith('<?xml'):
                formatted_xml = lines[0] + '\n' + '\n'.join(lines[1:])
            
            # 写入文件
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(formatted_xml)
            
            if new_urls:
                print(f"✓ 已添加 {len(new_urls)} 个新URL到sitemap:")
                for url in new_urls[:10]:  # 只显示前10个
                    print(f"  - {url}")
                if len(new_urls) > 10:
                    print(f"  ... 还有 {len(new_urls) - 10} 个URL")
            
            if updated_count > len(new_urls):
                print(f"✓ 已更新 {updated_count - len(new_urls)} 个现有URL的lastmod")
            
            return True
        else:
            print("✓ sitemap无需更新")
            return True
            
    except Exception as e:
        print(f"错误: 更新sitemap失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='使用指南更新脚本')
    parser.add_argument('--incremental', action='store_true', 
                       help='增量模式：只生成新增的文章（跳过已存在的HTML文件）')
    parser.add_argument('--full', action='store_true',
                       help='全量模式：重新生成所有文章（默认）')
    args = parser.parse_args()
    
    # 确定模式
    incremental = args.incremental and not args.full
    
    print("=" * 50)
    print("使用指南更新脚本")
    print("=" * 50)
    print(f"模式: {'增量生成（只生成新增）' if incremental else '全量生成（重新生成所有）'}")
    print()
    
    # 1. 加载数据
    print("1. 加载指南数据...")
    data = load_json(GUIDES_DATA_FILE)
    if not data:
        return
    
    articles = data.get('articles', [])
    print(f"   找到 {len(articles)} 篇指南")
    
    # 2. 确保目录存在
    os.makedirs(GUIDES_DIR, exist_ok=True)
    
    # 3. 生成详情页
    print(f"\n2. 生成详情页（{'增量' if incremental else '全量'}模式）...")
    template_path = os.path.join(GUIDES_DIR, 'guide-template.html')
    
    if not os.path.exists(template_path):
        print(f"错误: 模板文件不存在 {template_path}")
        return
    
    generated_count = 0
    skipped_count = 0
    
    for article in articles:
        article_id = article.get('id', '')
        if not article_id:
            continue
        
        output_path = os.path.join(GUIDES_DIR, f"{article_id}.html")
        
        # 增量模式：检查文件是否已存在
        if incremental and os.path.exists(output_path):
            print(f"  ⊘ 跳过（已存在）: {article_id}.html")
            skipped_count += 1
            continue
        
        # 生成HTML
        html = generate_article_page(article, template_path, all_articles=articles, output_path=output_path)
        if html:
            save_file(output_path, html)
            generated_count += 1
    
    print(f"\n   生成: {generated_count} 个文件")
    if incremental:
        print(f"   跳过: {skipped_count} 个已存在的文件")
    
    # 4. 更新sitemap
    print("\n3. 更新sitemap...")
    update_sitemap(articles, incremental=incremental)
    
    print("\n" + "=" * 50)
    print("更新完成！")
    print("=" * 50)
    print("\n下一步:")
    print("1. 检查生成的HTML文件")
    print("2. 上传到服务器")
    print("3. 提交sitemap到搜索引擎")

if __name__ == '__main__':
    main()

