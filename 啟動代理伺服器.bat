@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ========================================
echo   台灣股票分析工具 - 代理伺服器 v1.1
echo ========================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python，請先至 https://www.python.org/downloads/ 安裝
    pause
    exit /b 1
)

echo [1/2] 安裝/確認 requests 套件...
python -m pip install requests -q
echo.
echo [2/2] 啟動代理伺服器...
echo.
python stock_proxy.py
pause
