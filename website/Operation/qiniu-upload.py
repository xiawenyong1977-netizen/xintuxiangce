#!/usr/bin/env python3
"""
七牛云文件上传脚本
用于将安装包上传到七牛云对象存储
"""
import os
import sys
import json
import glob
import re
from pathlib import Path

try:
    from qiniu import Auth, put_file, BucketManager
    from qiniu import put_data
except ImportError:
    print("错误: 需要安装 qiniu 库")
    print("安装命令: pip install qiniu")
    sys.exit(1)

# 配置文件路径
CONFIG_FILE = 'qiniu-config.json'

def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        print(f"错误: 配置文件 {CONFIG_FILE} 不存在")
        print(f"请复制 qiniu-config.json.example 为 {CONFIG_FILE} 并填写配置")
        sys.exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def upload_file(q, bucket_name, local_file, remote_key):
    """上传单个文件"""
    token = q.upload_token(bucket_name, remote_key, 3600)
    
    try:
        ret, info = put_file(token, remote_key, local_file)
        if ret:
            print(f"✓ 上传成功: {remote_key}")
            return True
        else:
            print(f"✗ 上传失败: {remote_key} - {info}")
            return False
    except Exception as e:
        print(f"✗ 上传异常: {remote_key} - {str(e)}")
        return False

def extract_date_from_filename(filename):
    """从文件名中提取日期信息用于排序
    
    支持格式：
    - xtxc202511111206.zip -> 202511111206
    - xtxcsetup202511021528.zip -> 202511021528
    - xuxc202510311010.apk -> 202510311010
    """
    # 匹配文件名中的日期时间格式：YYYYMMDDHHMM 或 YYYYMMDD
    # 查找8位或12位数字（日期或日期+时间）
    match = re.search(r'(\d{8})(\d{4})?', filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2) if match.group(2) else '0000'
        return int(date_str + time_str)
    return 0

def get_files_to_upload(base_dir, config):
    """获取需要上传的文件列表"""
    files = []
    base_path = config.get('base_path', 'dist')
    
    # 定义要上传的目录和文件类型
    upload_patterns = [
        {
            'local_dir': os.path.join(base_dir, 'pc', 'portable'),
            'remote_prefix': 'pc/portable',
            'extensions': ['.zip']
        },
        {
            'local_dir': os.path.join(base_dir, 'pc', 'setup'),
            'remote_prefix': 'pc/setup',
            'extensions': ['.exe', '.zip']
        },
        {
            'local_dir': os.path.join(base_dir, 'android'),
            'remote_prefix': 'android',
            'extensions': ['.apk']
        }
    ]
    
    for pattern in upload_patterns:
        local_dir = pattern['local_dir']
        if not os.path.exists(local_dir):
            print(f"⚠ 目录不存在: {local_dir}")
            continue
        
        for ext in pattern['extensions']:
            file_pattern = os.path.join(local_dir, f'*{ext}')
            found_files = glob.glob(file_pattern)
            
            if not found_files:
                continue
            
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
            
            found_files.sort(key=sort_key, reverse=True)
            
            # 只选择最新的文件（每个扩展名只上传一个最新文件）
            latest_file = found_files[0]
            filename = os.path.basename(latest_file)
            remote_key = f"{pattern['remote_prefix']}/{filename}"
            files.append({
                'local': latest_file,
                'remote': remote_key,
                'size': os.path.getsize(latest_file)
            })
            
            # 如果有多个文件，提示哪些被跳过
            if len(found_files) > 1:
                skipped = [os.path.basename(f) for f in found_files[1:]]
                print(f"⚠ {local_dir}: 找到 {len(found_files)} 个文件，只上传最新的: {filename}")
                print(f"  跳过的文件: {', '.join(skipped)}")
    
    return files

def main():
    print("=== 七牛云文件上传工具 ===\n")
    
    # 加载配置
    config = load_config()
    access_key = config.get('access_key')
    secret_key = config.get('secret_key')
    bucket_name = config.get('bucket_name')
    
    if not access_key or not secret_key:
        print("错误: 请在配置文件中填写 access_key 和 secret_key")
        sys.exit(1)
    
    # 初始化七牛云认证
    q = Auth(access_key, secret_key)
    
    # 获取要上传的文件
    # 从配置文件获取 base_path，如果没有则使用默认值
    base_path = config.get('base_path', 'dist')
    # 脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建完整的 base_dir 路径
    base_dir = os.path.join(script_dir, base_path)
    
    if not os.path.exists(base_dir):
        print(f"错误: 源目录不存在: {base_dir}")
        print(f"提示: 请检查配置文件中的 base_path 设置，当前为: {base_path}")
        sys.exit(1)
    
    files = get_files_to_upload(base_dir, config)
    
    if not files:
        print("未找到需要上传的文件")
        return
    
    print(f"找到 {len(files)} 个文件需要上传:\n")
    total_size = 0
    for f in files:
        size_mb = f['size'] / (1024 * 1024)
        total_size += f['size']
        print(f"  - {f['remote']} ({size_mb:.2f} MB)")
    
    total_size_mb = total_size / (1024 * 1024)
    print(f"\n总大小: {total_size_mb:.2f} MB")
    
    # 确认上传
    confirm = input("\n是否开始上传? (y/n): ")
    if confirm.lower() != 'y':
        print("已取消")
        return
    
    # 开始上传
    print("\n开始上传...\n")
    success_count = 0
    fail_count = 0
    
    for f in files:
        if upload_file(q, bucket_name, f['local'], f['remote']):
            success_count += 1
        else:
            fail_count += 1
    
    # 输出结果
    print(f"\n=== 上传完成 ===")
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")
    
    if success_count > 0:
        domain = config.get('domain', '')
        if domain:
            print(f"\n文件访问地址:")
            for f in files:
                if os.path.exists(f['local']):
                    print(f"  {domain}/{f['remote']}")

if __name__ == '__main__':
    main()

