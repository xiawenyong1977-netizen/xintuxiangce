<?php
/**
 * 芯图相册 - 自动下载最新版本
 * 自动检测dist目录下最新的zip文件并提供下载
 */

// 配置
$distDir = '../dist/';
$allowedExtensions = ['zip', 'exe']; // 允许的文件扩展名
$preferExtension = 'zip'; // 优先下载的扩展名

// 获取dist目录下的所有文件
function getLatestFile($dir, $allowedExtensions, $preferExtension) {
    if (!is_dir($dir)) {
        return null;
    }
    
    $files = [];
    $handle = opendir($dir);
    
    while (($file = readdir($handle)) !== false) {
        if ($file == '.' || $file == '..') {
            continue;
        }
        
        $filePath = $dir . $file;
        if (!is_file($filePath)) {
            continue;
        }
        
        // 检查文件扩展名
        $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
        if (!in_array($ext, $allowedExtensions)) {
            continue;
        }
        
        $files[] = [
            'name' => $file,
            'path' => $filePath,
            'ext' => $ext,
            'time' => filemtime($filePath),
            'size' => filesize($filePath)
        ];
    }
    
    closedir($handle);
    
    if (empty($files)) {
        return null;
    }
    
    // 优先选择zip文件
    $preferFiles = array_filter($files, function($f) use ($preferExtension) {
        return $f['ext'] === $preferExtension;
    });
    
    if (!empty($preferFiles)) {
        $files = $preferFiles;
    }
    
    // 按修改时间排序，获取最新的
    usort($files, function($a, $b) {
        return $b['time'] - $a['time'];
    });
    
    return $files[0];
}

// 获取最新文件
$latestFile = getLatestFile($distDir, $allowedExtensions, $preferExtension);

if ($latestFile === null) {
    http_response_code(404);
    die('未找到可下载的文件');
}

// 如果是GET请求且带有info参数，返回文件信息（JSON）
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['info'])) {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        'success' => true,
        'filename' => $latestFile['name'],
        'size' => $latestFile['size'],
        'sizeFormatted' => formatBytes($latestFile['size']),
        'extension' => $latestFile['ext'],
        'modifiedTime' => date('Y-m-d H:i:s', $latestFile['time'])
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// 下载文件
$filePath = $latestFile['path'];
$fileName = $latestFile['name'];

// 设置下载头
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . $fileName . '"');
header('Content-Length: ' . filesize($filePath));
header('Cache-Control: no-cache, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

// 输出文件
readfile($filePath);

// 格式化文件大小
function formatBytes($bytes, $precision = 2) {
    $units = ['B', 'KB', 'MB', 'GB', 'TB'];
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($units) - 1);
    $bytes /= pow(1024, $pow);
    return round($bytes, $precision) . ' ' . $units[$pow];
}
?>

