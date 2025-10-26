#!/usr/bin/env python3
"""
芯图相册 - 自动下载便携版最新版本
"""
import os
import glob
import sys

def get_latest_portable():
    """获取便携版目录下最新的zip文件"""
    portable_dir = '/var/www/xintuxiangce/dist/pc/portable'
    
    if not os.path.exists(portable_dir):
        return None
    
    zip_files = glob.glob(os.path.join(portable_dir, '*.zip'))
    
    if not zip_files:
        return None
    
    # 按修改时间排序，获取最新的
    latest_file = max(zip_files, key=os.path.getmtime)
    return latest_file

def main():
    latest_file = get_latest_portable()
    
    if not latest_file:
        print("Status: 404 Not Found")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("<h1>404 - 未找到便携版文件</h1>")
        return
    
    filename = os.path.basename(latest_file)
    file_size = os.path.getsize(latest_file)
    
    # 设置下载头（注意：这些打印应该在输出文件内容之前）
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

