#!/usr/bin/env python3
"""
芯图相册 - 自动下载最新版本
通过参数判断下载便携版、安装版或Android版
"""
import os
import glob
import sys
import cgi

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

def main():
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
    
    # 获取文件信息
    filename = os.path.basename(latest_file)
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
