# 通用部署脚本 - PowerShell版本
# 支持增量部署和全量部署
# 使用方法：
#   增量部署指定目录：.\deploy.ps1 -TargetDir website
#   全量部署指定目录：.\deploy.ps1 -TargetDir website -Mode full
#   默认部署 website 目录：.\deploy.ps1

param(
    [Parameter(Mandatory=$false)]
    [string]$TargetDir = "website",
    
    [ValidateSet("incremental", "full")]
    [string]$Mode = "incremental"
)

$ErrorActionPreference = "Stop"

# ==================== 配置区域 ====================
$SERVER = "root@web"
$REMOTE_DIR = "/var/www/xintuxiangce"
$OWNER = "lighttpd:lighttpd"
$DEPLOY_MODE = $Mode
$TARGET_DIR = $TargetDir

# 需要部署的文件类型
$DEPLOY_EXTENSIONS = @("html", "css", "js", "json", "xml", "txt", "png", "jpg", "jpeg", "gif", "webp", "svg", "ico", "pdf")

# 需要排除的目录和文件模式
$EXCLUDE_PATTERNS = @(
    "__pycache__",
    "*.pyc",
    "*.md",
    "*.py",
    ".git",
    "*.sh",
    "*.bat",
    "*.ps1",
    "*.csv",
    "Operation",
    "*.bak",
    "*.tmp",
    "*.log",
    ".DS_Store",
    "Thumbs.db"
)

# ==================== 颜色输出函数 ====================
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# ==================== 检查依赖 ====================
function Test-Dependencies {
    Write-Info "检查依赖..."
    
    # 检查Git
    $gitCmd = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitCmd) {
        Write-Error "Git 未安装，请先安装 Git"
        exit 1
    }
    
    # 检查scp
    $scpCmd = Get-Command scp -ErrorAction SilentlyContinue
    if (-not $scpCmd) {
        Write-Error "scp 未安装，请先安装 OpenSSH"
        exit 1
    }
    
    # 检查ssh
    $sshCmd = Get-Command ssh -ErrorAction SilentlyContinue
    if (-not $sshCmd) {
        Write-Error "ssh 未安装，请先安装 OpenSSH"
        exit 1
    }
    
    Write-Success "依赖检查通过"
}

# ==================== Git 命令包装函数（抑制警告）====================
function Invoke-GitCommand {
    param(
        [string[]]$Arguments
    )
    
    # 临时设置 Git 配置以避免行尾符警告
    $oldSafecrlf = git config --get core.safecrlf 2>$null
    $oldAutocrlf = git config --get core.autocrlf 2>$null
    
    # 设置临时配置
    git config core.safecrlf false 2>$null | Out-Null
    git config core.autocrlf false 2>$null | Out-Null
    
    # 清除可能存在的 GIT_CONFIG_PARAMETERS 环境变量
    $oldConfigParam = $env:GIT_CONFIG_PARAMETERS
    $env:GIT_CONFIG_PARAMETERS = $null
    
    try {
        # 直接执行 Git 命令，捕获所有输出并过滤警告
        # 使用 *>&1 捕获所有输出流，然后过滤
        $output = & git $Arguments *>&1 | Where-Object { 
            if ($_ -is [System.Management.Automation.ErrorRecord]) {
                # 错误记录转换为字符串并检查
                $msg = $_.ToString()
                return $msg -notmatch 'warning:' -and $msg -notmatch 'LF will be replaced' -and $msg -notmatch 'CRLF'
            } else {
                # 普通输出
                return $_ -and $_ -notmatch 'warning:' -and $_ -notmatch 'LF will be replaced' -and $_ -notmatch 'CRLF'
            }
        } | ForEach-Object {
            # 如果是错误记录，转换为字符串；否则直接返回
            if ($_ -is [System.Management.Automation.ErrorRecord]) {
                $_.ToString()
            } else {
                $_
            }
        }
        
        # 确保返回数组
        if (-not $output) {
            $output = @()
        } elseif ($output -isnot [Array]) {
            $output = @($output)
        }
    } catch {
        # 如果出错，返回空数组
        $output = @()
    } finally {
        # 恢复环境变量
        $env:GIT_CONFIG_PARAMETERS = $oldConfigParam
    }
    
    # 恢复 Git 配置
    if ($oldSafecrlf) {
        git config core.safecrlf $oldSafecrlf 2>$null | Out-Null
    } else {
        git config --unset core.safecrlf 2>$null | Out-Null
    }
    if ($oldAutocrlf) {
        git config core.autocrlf $oldAutocrlf 2>$null | Out-Null
    } else {
        git config --unset core.autocrlf 2>$null | Out-Null
    }
    
    return $output
}

# ==================== 检查Git仓库 ====================
function Test-GitRepository {
    # 查找Git仓库根目录（向上查找）
    $gitRoot = $null
    $currentPath = (Get-Location).Path
    
    # 向上查找.git目录
    $checkPath = $currentPath
    while ($checkPath) {
        $gitPath = Join-Path $checkPath ".git"
        if (Test-Path $gitPath) {
            $gitRoot = $checkPath
            break
        }
        
        $parent = Split-Path $checkPath -Parent
        # 如果父目录和当前目录相同，说明到达根目录
        if ($parent -eq $checkPath -or -not $parent) {
            break
        }
        $checkPath = $parent
    }
    
    if (-not $gitRoot) {
        Write-Warning "未找到 Git 仓库，将使用全量部署模式"
        $script:DEPLOY_MODE = "full"
        return
    }
    
    Write-Info "找到 Git 仓库根目录: $gitRoot"
    
    # 切换到Git仓库根目录进行Git操作
    Push-Location $gitRoot
    try {
        # 检查是否有未提交的更改（抑制行尾符警告）
        $oldConfig = $env:GIT_CONFIG_PARAMETERS
        $env:GIT_CONFIG_PARAMETERS = $null
        
        # 临时设置 Git 配置，让 Git 不转义路径
        $oldQuotepath = git config --get core.quotepath 2>$null
        git config core.quotepath false 2>$null | Out-Null
        
        # 使用包装函数执行 Git 命令
        $statusOutput = Invoke-GitCommand -Arguments @("status", "--porcelain")
        
        # 恢复 Git 配置
        if ($oldQuotepath) {
            git config core.quotepath $oldQuotepath 2>$null | Out-Null
        } else {
            git config --unset core.quotepath 2>$null | Out-Null
        }
        
        $env:GIT_CONFIG_PARAMETERS = $oldConfig
        
        # 过滤掉包含警告信息的行，只保留实际的状态信息
        $status = $statusOutput | Where-Object { 
            $_ -and 
            $_ -match '^[ MADRCU?]{2}'  # 只保留以 Git 状态码开头的行
        }
        if ($status) {
            Write-Warning "检测到未提交的更改（这些更改将被包含在部署中）："
            Write-Host ""
            
            # 显示详细的更改信息（只显示前10个，避免输出过长）
            $displayCount = [Math]::Min($status.Count, 10)
            for ($i = 0; $i -lt $displayCount; $i++) {
                $line = $status[$i]
                $statusCode = $line.Substring(0, 2).Trim()
                $fileName = $line.Substring(3)
                
                # 解析状态码
                $staged = $statusCode[0]
                $unstaged = $statusCode[1]
                
                $statusText = ""
                if ($staged -eq "A") { $statusText += "[新增]" }
                if ($staged -eq "M") { $statusText += "[修改]" }
                if ($staged -eq "D") { $statusText += "[删除]" }
                if ($staged -eq "R") { $statusText += "[重命名]" }
                if ($unstaged -eq "M") { $statusText += "[工作区修改]" }
                if ($unstaged -eq "D") { $statusText += "[工作区删除]" }
                if ($staged -eq " " -and $unstaged -eq "?") { $statusText = "[未跟踪]" }
                
                Write-Host "  $statusText $fileName" -ForegroundColor Yellow
            }
            
            if ($status.Count -gt 10) {
                Write-Info "... 还有 $($status.Count - 10) 个文件有未提交的更改"
            }
            Write-Host ""
            Write-Info "提示：将在下一步显示实际要部署的文件列表"
        }
    } finally {
        Pop-Location
    }
}

# ==================== 查找Git仓库根目录 ====================
function Get-GitRoot {
    $currentPath = (Get-Location).Path
    $checkPath = $currentPath
    
    while ($checkPath) {
        $gitPath = Join-Path $checkPath ".git"
        if (Test-Path $gitPath) {
            return $checkPath
        }
        
        $parent = Split-Path $checkPath -Parent
        # 如果父目录和当前目录相同，说明到达根目录
        if ($parent -eq $checkPath -or -not $parent) {
            break
        }
        $checkPath = $parent
    }
    
    return $null
}

# ==================== 获取变更文件列表 ====================
function Get-ChangedFiles {
    if ($DEPLOY_MODE -eq "full") {
        Write-Info "全量部署模式：获取所有文件..."
        
        # 获取所有需要部署的文件
        $files = Get-ChildItem -Recurse -File | Where-Object {
            $ext = $_.Extension.TrimStart('.')
            $ext -in $DEPLOY_EXTENSIONS
        } | Where-Object {
            $exclude = $false
            foreach ($pattern in $EXCLUDE_PATTERNS) {
                if ($_.FullName -like "*$pattern*") {
                    $exclude = $true
                    break
                }
            }
            -not $exclude
        } | ForEach-Object {
            $_.FullName.Replace((Get-Location).Path + "\", "").Replace("\", "/")
        }
        
        return $files | Sort-Object
    } else {
        Write-Info "增量部署模式：检测 Git 变更文件..."
        Write-Info "  检测范围：工作区所有变更（包括已暂存和未暂存的文件）"
        
        # 查找Git仓库根目录
        $gitRoot = Get-GitRoot
        if (-not $gitRoot) {
            Write-Warning "未找到 Git 仓库，切换到全量部署模式"
            $script:DEPLOY_MODE = "full"
            return Get-ChangedFiles
        }
        
        # 切换到Git仓库根目录执行Git命令
        Push-Location $gitRoot
        try {
            # 获取工作区相对于HEAD的所有变更文件（包括已暂存和未暂存的）
            # git diff HEAD 会显示工作区相对于HEAD的所有差异，包括：
            # - 已暂存（staged）的变更
            # - 未暂存（unstaged）的变更
            # --diff-filter=ACMR 只包含：Added, Copied, Modified, Renamed
            $oldConfig = $env:GIT_CONFIG_PARAMETERS
            $env:GIT_CONFIG_PARAMETERS = $null
            
            # 临时设置 Git 配置，让 Git 不转义路径（避免 \345\244\247 这样的转义序列）
            $oldQuotepath = git config --get core.quotepath 2>$null
            git config core.quotepath false 2>$null | Out-Null
            
            # 使用包装函数执行 Git 命令
            $changedOutput = Invoke-GitCommand -Arguments @("diff", "--name-only", "--diff-filter=ACMR", "HEAD")
            
            # 过滤掉包含警告信息的行，只保留文件名
            $changed = $changedOutput | Where-Object { 
                $_ -and 
                $_.Trim() -ne '' -and
                $_ -notmatch '^git:'  # 排除 Git 错误信息
            }
            if (-not $changed) {
                $changed = @()
            }
            
            # 同时获取未跟踪的新文件（Untracked files）
            # 这些文件不在HEAD中，但存在于工作区
            $untrackedOutput = Invoke-GitCommand -Arguments @("ls-files", "--others", "--exclude-standard")
            
            # 过滤掉包含警告信息的行，只保留文件名
            $untracked = $untrackedOutput | Where-Object { 
                $_ -and 
                $_.Trim() -ne '' -and
                $_ -notmatch '^git:'  # 排除 Git 错误信息
            }
            if (-not $untracked) {
                $untracked = @()
            }
            
            # 恢复 Git 配置
            if ($oldQuotepath) {
                git config core.quotepath $oldQuotepath 2>$null | Out-Null
            } else {
                git config --unset core.quotepath 2>$null | Out-Null
            }
            
            $env:GIT_CONFIG_PARAMETERS = $oldConfig
            
            # 合并并去重
            $allChanged = ($changed + $untracked) | Select-Object -Unique
            
            # 将文件路径转换为相对于目标目录的路径
            # 获取目标目录的完整路径（相对于 Git 根目录）
            $targetDirFullPath = Join-Path $gitRoot $TARGET_DIR
            $targetDirName = Split-Path $TARGET_DIR -Leaf
            
            $allChanged = $allChanged | ForEach-Object {
                try {
                    # Git返回的路径是相对于Git根目录的
                    $gitRelativePath = $_.Trim()
                    if (-not $gitRelativePath) {
                        return $null
                    }
                    
                    # 只处理目标目录下的文件
                    if ($gitRelativePath -notlike "$targetDirName/*" -and $gitRelativePath -ne $targetDirName) {
                        return $null
                    }
                    
                    # 构建完整路径
                    $fullPath = Join-Path $gitRoot $gitRelativePath
                    
                    # 使用 -LiteralPath 和错误处理来避免路径中的转义字符问题
                    $exists = $false
                    try {
                        $exists = Test-Path -LiteralPath $fullPath -ErrorAction Stop
                    } catch {
                        # 如果路径无效，尝试使用普通路径检查
                        try {
                            $exists = Test-Path $fullPath -ErrorAction Stop
                        } catch {
                            # 路径无效，跳过
                            return $null
                        }
                    }
                    
                    if ($exists) {
                        # 检查文件是否在目标目录下
                        if ($fullPath -notlike "$targetDirFullPath\*") {
                            # 文件不在目标目录下，跳过
                            return $null
                        }
                        
                        # 转换为相对于目标目录的路径
                        $relativePath = $fullPath.Replace($targetDirFullPath + "\", "").Replace("\", "/")
                        
                        # 如果路径仍然包含绝对路径（说明转换失败），跳过
                        if ($relativePath -match '^[A-Z]:') {
                            return $null
                        }
                        
                        $relativePath
                    }
                } catch {
                    # 跳过无效路径，不显示错误
                    return $null
                }
            } | Where-Object { $_ }
        } finally {
            Pop-Location
        }
        
        if (-not $allChanged) {
            Write-Warning "没有检测到变更文件"
            $response = Read-Host "是否使用全量部署？(y/n)"
            if ($response -eq "y" -or $response -eq "Y") {
                $script:DEPLOY_MODE = "full"
                return Get-ChangedFiles
            } else {
                Write-Info "部署已取消"
                exit 0
            }
        }
        
        # 过滤出需要部署的文件
        $files = $allChanged | Where-Object {
            if (-not (Test-Path $_)) {
                return $false
            }
            
            $ext = [System.IO.Path]::GetExtension($_).TrimStart('.')
            if ($ext -notin $DEPLOY_EXTENSIONS) {
                return $false
            }
            
            $exclude = $false
            foreach ($pattern in $EXCLUDE_PATTERNS) {
                if ($_ -like "*$pattern*") {
                    $exclude = $true
                    break
                }
            }
            
            return -not $exclude
        }
        
        return $files
    }
}

# ==================== 上传文件 ====================
function Upload-Files {
    param([array]$Files)
    
    Write-Info "开始上传文件..."
    
    $count = 0
    $failed = 0
    
    foreach ($file in $Files) {
        if (-not $file) {
            continue
        }
        
        # 计算远程路径（需要包含目标目录名）
        $targetDirName = Split-Path $TARGET_DIR -Leaf
        $remotePath = "$REMOTE_DIR/$targetDirName/$file"
        
        # 计算远程目录（处理 Unix 路径）
        $remoteDir = $remotePath
        if ($remotePath.Contains("/")) {
            $parts = $remotePath -split "/"
            $remoteDir = $parts[0..($parts.Length-2)] -join "/"
        }
        
        # 确保远程目录存在（如果文件不在根目录）
        if ($remoteDir -ne $REMOTE_DIR) {
            $sshResult = ssh $SERVER "mkdir -p '$remoteDir'" 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "创建远程目录失败: $remoteDir"
                Write-Warning "错误信息: $sshResult"
            }
        }
        
        # 上传文件（文件路径相对于当前目录）
        $localFile = $file.Replace("/", "\")
        $localFilePath = Join-Path (Get-Location).Path $localFile
        
        # 检查本地文件是否存在
        if (-not (Test-Path $localFilePath)) {
            Write-Warning "本地文件不存在: $localFilePath"
            $failed++
            continue
        }
        
        # 上传文件
        $scpResult = scp $localFilePath "${SERVER}:${remotePath}" 2>&1
        if ($LASTEXITCODE -eq 0) {
            $count++
            Write-Success "✓ $file"
        } else {
            $failed++
            Write-Error "✗ $file"
            Write-Error "  错误: $scpResult"
        }
    }
    
    Write-Info "上传完成：成功 $count 个，失败 $failed 个"
}

# ==================== 设置权限 ====================
function Set-FilePermissions {
    param([array]$Files)
    
    Write-Info "设置文件权限..."
    
    # 收集所有需要设置权限的目录
    $dirs = $Files | ForEach-Object {
        $dir = Split-Path $_ -Parent
        if ($dir -and $dir -ne ".") {
            $dir
        }
    } | Select-Object -Unique
    
    # 获取目标目录名
    $targetDirName = Split-Path $TARGET_DIR -Leaf
    
    foreach ($dir in $dirs) {
        $remoteDir = "$REMOTE_DIR/$targetDirName/$dir"
        ssh $SERVER "chown -R $OWNER '$remoteDir' 2>/dev/null; chmod -R 755 '$remoteDir' 2>/dev/null" 2>$null | Out-Null
    }
    
    # 设置文件权限
    foreach ($file in $Files) {
        if ($file) {
            $remoteFile = "$REMOTE_DIR/$targetDirName/$file"
            ssh $SERVER "chown $OWNER '$remoteFile' 2>/dev/null; chmod 644 '$remoteFile' 2>/dev/null" 2>$null | Out-Null
        }
    }
    
    Write-Success "权限设置完成"
}

# ==================== 主函数 ====================
function Main {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  通用部署脚本" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Info "部署模式: $DEPLOY_MODE"
    Write-Info "目标目录: $TARGET_DIR"
    Write-Info "服务器: $SERVER"
    Write-Info "远程目录: $REMOTE_DIR"
    Write-Host ""
    
    # 检查依赖
    Test-Dependencies
    
    # 检查目标目录是否存在
    $targetPath = Join-Path (Get-Location).Path $TARGET_DIR
    if (-not (Test-Path $targetPath)) {
        Write-Error "目标目录不存在: $targetPath"
        exit 1
    }
    
    # 切换到目标目录
    Push-Location $targetPath
    
    try {
        # 检查Git仓库（在切换到脚本目录后）
        Test-GitRepository
        # 获取变更文件
        $changedFiles = Get-ChangedFiles
        
        if (-not $changedFiles) {
            Write-Error "没有需要部署的文件"
            exit 1
        }
        
        # 显示将要部署的文件
        $fileCount = ($changedFiles | Measure-Object).Count
        Write-Info "准备部署 $fileCount 个文件："
        $changedFiles | Select-Object -First 20 | ForEach-Object { Write-Host "  $_" }
        if ($fileCount -gt 20) {
            Write-Info "... 还有 $($fileCount - 20) 个文件"
        }
        Write-Host ""
        
        # 确认部署
        $response = Read-Host "确认部署？(y/n)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Info "部署已取消"
            exit 0
        }
        
        # 上传文件
        Upload-Files -Files $changedFiles
        
        # 设置权限
        Set-FilePermissions -Files $changedFiles
        
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Green
        Write-Success "部署完成！"
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host ""
        Write-Info "验证部署："
        Write-Info "访问 https://www.xintuxiangce.top 查看网站"
    } finally {
        Pop-Location
    }
}

# 运行主函数
Main

