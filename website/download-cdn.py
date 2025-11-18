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
import urllib.request
import urllib.error

# CDN配置
CDN_CONFIG_FILE = '/var/www/xintuxiangce/website/qiniu-config.json'
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
    
    # 按修改时间排序，获取最新的
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def get_remote_path(file_type, filename):
    """获取CDN远程路径"""
    path_map = {
        'portable': f'pc/portable/{filename}',
        'setup': f'pc/setup/{filename}',
        'android': f'android/{filename}',
        'mac': f'mac/{filename}'
    }
    return path_map.get(file_type, '')

def redirect_to_cdn(cdn_url):
    """重定向到CDN"""
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

def serve_from_source(file_path, filename):
    """从源站提供文件下载"""
    file_size = os.path.getsize(file_path)
    
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
        with open(file_path, 'rb') as f:
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

def main():
    # 加载CDN配置
    cdn_available = load_cdn_config()
    
    # 获取参数
    form = cgi.FieldStorage()
    file_type = form.getvalue('type', 'portable').lower()
    
    # 根据类型确定目录
    base_dir = '/var/www/xintuxiangce/dist'
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
    
    # 如果CDN可用，尝试从CDN下载
    if cdn_available and CDN_DOMAIN:
        remote_path = get_remote_path(file_type, filename)
        if remote_path:
            cdn_url = f"{CDN_DOMAIN}/{remote_path}"
            
            # 检查CDN是否可用
            if check_cdn_available(cdn_url):
                redirect_to_cdn(cdn_url)
                return
            elif not FALLBACK_TO_SOURCE:
                print("Status: 503 Service Unavailable")
                print("Content-Type: text/html; charset=utf-8")
                print()
                print("<h1>503 - CDN服务暂时不可用</h1>")
                return
    
    # 回退到源站下载
    serve_from_source(latest_file, filename)

if __name__ == '__main__':
    main()

