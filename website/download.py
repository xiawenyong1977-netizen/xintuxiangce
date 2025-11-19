#!/usr/bin/env python3
"""
芯图相册 - 支持CDN的自动下载脚本
优先从CDN下载，如果CDN不可用则回退到源站
"""
import os
import glob
import sys
import cgi
import json
import re
import urllib.request
import urllib.error

# CDN配置
CDN_CONFIG_FILE = '/var/www/xintuxiangce/qiniu-config.json'
CDN_DOMAIN = None
CDN_ENABLED = False
FALLBACK_TO_SOURCE = True

def load_cdn_config():
    """加载CDN配置"""
    global CDN_DOMAIN, CDN_ENABLED, FALLBACK_TO_SOURCE
    
    if not os.path.exists(CDN_CONFIG_FILE):
        return False
    
    try:
        with open(CDN_CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            CDN_DOMAIN = config.get('domain', '').rstrip('/')
            CDN_ENABLED = config.get('cdn_enabled', False)
            FALLBACK_TO_SOURCE = config.get('fallback_to_source', True)
            return CDN_ENABLED and CDN_DOMAIN
    except Exception as e:
        print(f"# CDN配置加载失败: {str(e)}", file=sys.stderr)
        return False

def check_cdn_available(cdn_url):
    """检查CDN是否可用"""
    try:
        req = urllib.request.Request(cdn_url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except:
        return False

def get_remote_path(file_type, filename):
    """获取CDN远程路径"""
    path_map = {
        'portable': f'pc/portable/{filename}',
        'setup': f'pc/setup/{filename}',
        'android': f'android/{filename}',
        'mac': f'mac/{filename}'
    }
    return path_map.get(file_type, '')

def increment_download_count(download_type):
    """
    调用下载量统计接口（同步调用，超时时间短，不阻塞下载）
    
    注意：在 CGI 环境中，daemon 线程可能在脚本退出前被终止，
    所以使用同步调用，但设置很短的超时时间（1秒），确保不影响下载流程。
    
    Args:
        download_type: 'android' 或 'windows'
    """
    try:
        api_url = f"https://api.aifuture.net.cn/api/v1/stats/download-count/increment/public?download_type={download_type}"
        
        req = urllib.request.Request(api_url, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'XintuXiangce-Download/1.0')
        
        # 使用较短的超时时间（2秒），确保不影响下载流程
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                if data.get('success'):
                    print(f"# 下载量统计成功: {download_type}", file=sys.stderr)
                    return True
            else:
                print(f"# 下载量统计失败: HTTP {response.status}", file=sys.stderr)
    except urllib.error.URLError as e:
        # 网络错误或超时，静默处理
        print(f"# 下载量统计网络错误（不影响下载）: {str(e)}", file=sys.stderr)
    except Exception as e:
        # 其他异常，静默处理
        print(f"# 下载量统计异常（不影响下载）: {str(e)}", file=sys.stderr)
    
    return False

def is_crawler():
    """
    检测当前请求是否来自爬虫
    
    Returns:
        True 如果是爬虫，False 如果是正常用户
    """
    user_agent = os.environ.get('HTTP_USER_AGENT', '').lower()
    
    if not user_agent:
        # 没有 User-Agent 的请求很可能是爬虫
        return True
    
    # 常见爬虫标识
    crawler_keywords = [
        'bot', 'crawler', 'spider', 'scraper',
        'googlebot', 'bingbot', 'slurp', 'duckduckbot',
        'baiduspider', 'yandexbot', 'sogou', 'exabot',
        'facebot', 'ia_archiver', 'archive.org_bot',
        'msnbot', 'ahrefsbot', 'semrushbot', 'dotbot',
        'mj12bot', 'megaindex', 'blexbot', 'petalbot',
        'curl', 'wget', 'python-requests', 'scrapy',
        'http', 'java', 'go-http-client', 'okhttp',
        'apache-httpclient', 'postman', 'insomnia'
    ]
    
    # 检查 User-Agent 是否包含爬虫关键词
    for keyword in crawler_keywords:
        if keyword in user_agent:
            return True
    
    return False

def get_download_type_for_stats(file_type):
    """
    将文件类型映射为统计接口需要的下载类型
    
    Args:
        file_type: 'portable', 'setup', 'android', 'mac'
    
    Returns:
        'android', 'windows', 或 None（不统计）
    """
    if file_type == 'android':
        return 'android'
    elif file_type in ('portable', 'setup'):
        return 'windows'
    else:
        return None  # mac 或其他类型不统计

def redirect_to_cdn(cdn_url, file_type):
    """重定向到CDN，并统计下载量"""
    # 统计下载量（此时已确认不是爬虫）
    download_type = get_download_type_for_stats(file_type)
    if download_type:
        increment_download_count(download_type)
    
    print("Status: 302 Found")
    print(f"Location: {cdn_url}")
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(f"""<html>
<head>
    <meta http-equiv="refresh" content="0;url={cdn_url}">
    <title>正在跳转...</title>
</head>
<body>
    <p>正在跳转到下载地址...</p>
    <p>如果未自动跳转，请<a href="{cdn_url}">点击这里</a></p>
</body>
</html>""")

def extract_date_from_filename(filename):
    """从文件名中提取日期信息用于排序
    
    支持格式：
    - xtxc202511111206.zip -> 202511111206
    - xtxcsetup202511021528.zip -> 202511021528
    - xuxc202510311010.apk -> 202510311010
    """
    # 匹配文件名中的日期时间格式：YYYYMMDDHHMM 或 YYYYMMDD
    match = re.search(r'(\d{8})(\d{4})?', filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2) if match.group(2) else '0000'
        return int(date_str + time_str)
    return 0

def get_latest_file(dir_path):
    """获取指定目录下最新的文件"""
    if not os.path.exists(dir_path):
        return None
    
    # 支持 .zip, .exe, .apk 等文件格式
    pattern = os.path.join(dir_path, '*.*')
    files = glob.glob(pattern)
    
    # 过滤掉不是压缩包或安装文件的文件
    ext_patterns = ['.zip', '.exe', '.apk', '.dmg', '.pkg']
    files = [f for f in files if any(f.lower().endswith(ext) for ext in ext_patterns)]
    
    if not files:
        return None
    
    # 优先按文件名中的日期排序，如果无法提取日期则按修改时间排序
    def sort_key(filepath):
        filename = os.path.basename(filepath)
        date_value = extract_date_from_filename(filename)
        if date_value > 0:
            # 如果能从文件名提取日期，使用日期排序（大的在前，即最新的在前）
            return (1, date_value)  # 1表示优先级高
        else:
            # 如果无法提取日期，使用修改时间排序
            return (0, os.path.getmtime(filepath))  # 0表示优先级低
    
    files.sort(key=sort_key, reverse=True)
    return files[0]

def main():
    # 加载CDN配置
    cdn_available = load_cdn_config()
    
    # 获取参数
    form = cgi.FieldStorage()
    file_type = form.getvalue('type', 'portable').lower()
    
    # 根据类型确定目录
    base_dir = '/var/www/xintuxiangce/website/dist'
    dirs = {
        'portable': os.path.join(base_dir, 'pc', 'portable'),
        'setup': os.path.join(base_dir, 'pc', 'setup'),
        'android': os.path.join(base_dir, 'android'),
        'mac': os.path.join(base_dir, 'mac')
    }
    
    # 如果是 Mac，返回正在开发中的提示
    if file_type == 'mac':
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>正在开发中</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    max-width: 500px;
                    margin: 0 auto;
                }
                h1 { margin-bottom: 20px; }
                p { font-size: 18px; line-height: 1.6; }
                a { color: white; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚧 Mac 版本正在开发中</h1>
                <p>感谢您的关注！Mac 版本正在紧锣密鼓地开发中，预计很快将与您见面。</p>
                <p>您可以先尝试使用便携版或联系我们的团队了解更多信息。</p>
                <p style="margin-top: 30px;">
                    <a href="/">&larr; 返回首页</a>
                </p>
            </div>
        </body>
        </html>
        """)
        return
    
    # 获取目标目录
    target_dir = dirs.get(file_type)
    
    if not target_dir:
        print("Status: 400 Bad Request")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("<h1>400 - 无效的下载类型</h1>")
        return
    
    # 获取最新文件
    latest_file = get_latest_file(target_dir)
    
    if not latest_file:
        print("Status: 404 Not Found")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print(f"<h1>404 - 未找到 {file_type} 版本文件</h1>")
        return
    
    filename = os.path.basename(latest_file)
    
    # 如果是爬虫，返回友好提示，不提供下载
    if is_crawler():
        print("Status: 403 Forbidden")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("""<html>
<head>
    <meta charset="UTF-8">
    <title>访问受限</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            max-width: 500px;
            margin: 0 auto;
        }
        h1 { margin-bottom: 20px; }
        p { font-size: 18px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 访问受限</h1>
        <p>抱歉，此下载链接仅对真实用户开放。</p>
        <p>如果您是真实用户，请使用浏览器访问我们的网站进行下载。</p>
    </div>
</body>
</html>""")
        return
    
    # 如果CDN可用，尝试从CDN下载
    if cdn_available and CDN_DOMAIN:
        remote_path = get_remote_path(file_type, filename)
        if remote_path:
            cdn_url = f"{CDN_DOMAIN}/{remote_path}"
            
            # 检查CDN是否可用
            if check_cdn_available(cdn_url):
                redirect_to_cdn(cdn_url, file_type)
                return
            elif not FALLBACK_TO_SOURCE:
                print("Status: 503 Service Unavailable")
                print("Content-Type: text/html; charset=utf-8")
                print()
                print("<h1>503 - CDN服务暂时不可用</h1>")
                return
    
    # 回退到源站下载
    # 统计下载量（此时已确认不是爬虫）
    download_type = get_download_type_for_stats(file_type)
    if download_type:
        increment_download_count(download_type)
    
    file_size = os.path.getsize(latest_file)
    
    # 设置下载头
    sys.stdout.write("Content-Type: application/octet-stream\r\n")
    sys.stdout.write(f"Content-Disposition: attachment; filename=\"{filename}\"\r\n")
    sys.stdout.write(f"Content-Length: {file_size}\r\n")
    sys.stdout.write("Cache-Control: no-cache, must-revalidate\r\n")
    sys.stdout.write("Pragma: no-cache\r\n")
    sys.stdout.write("Expires: 0\r\n")
    sys.stdout.write("\r\n")
    sys.stdout.flush()
    
    # 输出文件内容
    try:
        with open(latest_file, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sys.stdout.buffer.write(chunk)
    except Exception as e:
        print("Status: 500 Internal Server Error")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print(f"<h1>500 - 服务器错误</h1><p>{str(e)}</p>")

if __name__ == '__main__':
    main()
