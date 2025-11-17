# PowerShell 启动脚本
Write-Host "正在启动本地测试服务器..." -ForegroundColor Green
Write-Host ""
Write-Host "服务器将在以下地址启动：" -ForegroundColor Yellow
Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

# 切换到脚本所在目录
Set-Location $PSScriptRoot

# 启动服务器
python -m http.server 8000

