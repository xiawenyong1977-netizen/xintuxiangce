#!/usr/bin/env python3
"""
自动更新下载信息脚本
扫描dist目录，自动更新download-info.json文件
"""

import os
import json
import glob
from datetime import datetime
import hashlib

def get_file_checksum(filepath):
    """计算文件SHA256校验和"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return f"sha256:{sha256_hash.hexdigest()}"
    except:
        return "sha256:unknown"

def get_latest_zip_file():
    """获取dist目录下最新的zip文件"""
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        print(f"错误：{dist_dir} 目录不存在")
        return None
    
    # 查找所有zip文件
    zip_files = glob.glob(os.path.join(dist_dir, "*.zip"))
    if not zip_files:
        print("错误：dist目录下没有找到zip文件")
        return None
    
    # 按修改时间排序，获取最新的
    latest_file = max(zip_files, key=os.path.getmtime)
    return latest_file

def update_download_info():
    """更新下载信息"""
    latest_file = get_latest_zip_file()
    if not latest_file:
        return False
    
    # 获取文件信息
    filename = os.path.basename(latest_file)
    file_size = os.path.getsize(latest_file)
    file_size_mb = round(file_size / (1024 * 1024), 1)
    mod_time = os.path.getmtime(latest_file)
    mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
    
    # 提取版本信息（从文件名）
    if "xtxc" in filename:
        version = "v1.0.0"  # 可以根据实际版本调整
    else:
        version = "v1.0.0"
    
    # 计算校验和
    checksum = get_file_checksum(latest_file)
    
    # 构建新的下载信息
    download_info = {
        "latest": {
            "filename": filename,
            "displayName": "芯图相册 Windows版",
            "version": version,
            "size": file_size_mb,
            "sizeUnit": "MB",
            "releaseDate": mod_date,
            "downloadPath": f"dist/{filename}",
            "checksum": checksum,
            "description": "最新版本，包含所有功能优化和bug修复"
        },
        "history": [
            {
                "filename": filename,
                "version": version,
                "releaseDate": mod_date,
                "size": file_size_mb
            }
        ],
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 读取现有文件，保留历史记录
    json_file = "website/download-info.json"
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                # 保留历史记录，但更新最新文件
                if "history" in existing_data:
                    download_info["history"] = existing_data["history"]
                    # 如果新文件不在历史中，添加到开头
                    if not any(h["filename"] == filename for h in download_info["history"]):
                        download_info["history"].insert(0, {
                            "filename": filename,
                            "version": version,
                            "releaseDate": mod_date,
                            "size": file_size_mb
                        })
                        # 只保留最近5个版本
                        download_info["history"] = download_info["history"][:5]
        except:
            pass
    
    # 写入新文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(download_info, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新成功！")
    print(f"📁 文件: {filename}")
    print(f"📊 大小: {file_size_mb} MB")
    print(f"📅 日期: {mod_date}")
    print(f"🔗 路径: dist/{filename}")
    
    return True

if __name__ == "__main__":
    print("🚀 开始更新下载信息...")
    success = update_download_info()
    if success:
        print("✨ 下载信息更新完成！")
    else:
        print("❌ 更新失败！")
