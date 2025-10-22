/**
 * 简单的下载API - 自动检测最新文件
 * 可以直接在浏览器中访问，返回JSON格式的下载信息
 */

// 预定义的文件列表（按时间倒序排列）
const fileList = [
    {
        filename: "xtxc202510151254.zip",
        version: "v1.0.0",
        size: 275,
        date: "2025-10-15",
        path: "dist/pc/portable/xtxc202510151254.zip",
        type: "portable"
    },
    {
        filename: "xtxc202510151254-setup.exe",
        version: "v1.0.0",
        size: 280,
        date: "2025-10-15",
        path: "dist/pc/setup/xtxc202510151254-setup.exe",
        type: "setup"
    },
    {
        filename: "xtxc202510111614.zip", 
        version: "v0.9.0",
        size: 275,
        date: "2025-10-11",
        path: "dist/pc/portable/xtxc202510111614.zip",
        type: "portable"
    },
    {
        filename: "xtxc202510111614-setup.exe", 
        version: "v0.9.0",
        size: 280,
        date: "2025-10-11",
        path: "dist/pc/setup/xtxc202510111614-setup.exe",
        type: "setup"
    }
];

// 返回JSON格式的下载信息
function getDownloadInfo() {
    const latest = fileList[0];
    
    return {
        success: true,
        latest: {
            filename: latest.filename,
            displayName: "芯图相册 Windows便携版",
            version: latest.version,
            size: latest.size,
            sizeUnit: "MB",
            releaseDate: latest.date,
            downloadPath: latest.path,
            type: latest.type,
            description: "最新便携版本，包含所有功能优化和bug修复"
        },
        history: fileList,
        lastUpdated: new Date().toISOString()
    };
}

// 如果在浏览器环境中运行
if (typeof window !== 'undefined') {
    // 浏览器环境 - 可以作为JavaScript模块导入
    window.DownloadAPI = { getDownloadInfo };
} else {
    // Node.js环境 - 可以作为API服务运行
    console.log(JSON.stringify(getDownloadInfo(), null, 2));
}
