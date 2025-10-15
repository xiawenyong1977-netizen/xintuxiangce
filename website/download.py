#!/usr/bin/env python3
"""
芯图相册 - 自动下载最新版本
自动扫描dist目录，下载最新的zip文件
"""

import os
import glob
import sys
from datetime import datetime

def get_latest_zip():
    """获取dist目录下最新的zip文件"""
    dist_dir = '/var/www/xintuxiangce/dist/'
    
    if not os.path.exists(dist_dir):
        return None
    
    # 查找所有zip文件
    zip_files = glob.glob(os.path.join(dist_dir, '*.zip'))
    
    if not zip_files:
        return None
    
    # 按修改时间排序，获取最新的
    latest_file = max(zip_files, key=os.path.getmtime)
    return latest_file

def main():
    # 获取最新文件
    latest_file = get_latest_zip()
    
    if not latest_file:
        # 没有找到文件，返回404
        print("Status: 404 Not Found")
        print("Content-Type: text/html; charset=utf-8")
        print()
        print("<h1>404 - 未找到可下载的文件</h1>")
        return
    
    # 获取文件信息
    filename = os.path.basename(latest_file)
    file_size = os.path.getsize(latest_file)
    
    # 设置下载头
    print("Content-Type: application/octet-stream")
    print(f"Content-Disposition: attachment; filename=\"{filename}\"")
    print(f"Content-Length: {file_size}")
    print("Cache-Control: no-cache, must-revalidate")
    print("Pragma: no-cache")
    print("Expires: 0")
    print()
    
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
