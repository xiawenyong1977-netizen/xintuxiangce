@echo off
echo 正在启动本地测试服务器...
echo.
echo 服务器将在以下地址启动：
echo http://localhost:8000
echo.
echo 按 Ctrl+C 停止服务器
echo.
cd /d %~dp0
python -m http.server 8000

