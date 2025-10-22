#!/usr/bin/env python3
"""
测试脚本 - 检查文件检测功能
"""

import os
import glob

def test_file_detection():
    """测试文件检测功能"""
    dist_dir = '/var/www/xintuxiangce/dist/'
    
    print(f"检查目录: {dist_dir}")
    print(f"目录存在: {os.path.exists(dist_dir)}")
    
    if not os.path.exists(dist_dir):
        print("❌ dist目录不存在")
        return None
    
    # 检查便携版目录
    portable_dir = os.path.join(dist_dir, 'pc', 'portable')
    print(f"便携版目录: {portable_dir}")
    print(f"便携版目录存在: {os.path.exists(portable_dir)}")
    
    if os.path.exists(portable_dir):
        zip_files = glob.glob(os.path.join(portable_dir, '*.zip'))
        print(f"找到的zip文件: {zip_files}")
        
        if zip_files:
            # 按修改时间排序，获取最新的
            latest_file = max(zip_files, key=os.path.getmtime)
            file_size = os.path.getsize(latest_file)
            print(f"✅ 最新文件: {latest_file}")
            print(f"文件大小: {file_size} bytes ({file_size/1024/1024:.1f} MB)")
            return latest_file
    
    # 检查安装版目录
    setup_dir = os.path.join(dist_dir, 'pc', 'setup')
    print(f"安装版目录: {setup_dir}")
    print(f"安装版目录存在: {os.path.exists(setup_dir)}")
    
    if os.path.exists(setup_dir):
        zip_files = glob.glob(os.path.join(setup_dir, '*.zip'))
        print(f"找到的安装版文件: {zip_files}")
    
    print("❌ 未找到可下载的文件")
    return None

if __name__ == '__main__':
    test_file_detection()
