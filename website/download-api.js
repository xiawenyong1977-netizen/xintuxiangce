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
        path: "dist/xtxc202510151254.zip"
    },
    {
        filename: "xtxc202510111614.zip", 
        version: "v0.9.0",
        size: 275,
        date: "2025-10-11",
        path: "dist/xtxc202510111614.zip"
    }
];

// 返回JSON格式的下载信息
function getDownloadInfo() {
    const latest = fileList[0];
    
    return {
        success: true,
        latest: {
            filename: latest.filename,
            displayName: "芯图相册 Windows版",
            version: latest.version,
            size: latest.size,
            sizeUnit: "MB",
            releaseDate: latest.date,
            downloadPath: latest.path,
            description: "最新版本，包含所有功能优化和bug修复"
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
