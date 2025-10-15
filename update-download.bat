@echo off
echo 🚀 正在更新下载信息...

REM 运行Python脚本更新下载信息
python update-download-info.py

REM 如果Python脚本成功，部署到服务器
if %errorlevel% equ 0 (
    echo 📤 正在部署到服务器...
    scp website/download-info.json root@123.57.68.4:/var/www/xintuxiangce/
    scp website/script.js root@123.57.68.4:/var/www/xintuxiangce/
    echo ✅ 部署完成！
) else (
    echo ❌ 更新失败，请检查错误信息
)

pause
