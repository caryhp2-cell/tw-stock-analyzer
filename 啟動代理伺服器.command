#!/bin/bash
# 台灣股票分析工具 — 代理伺服器啟動腳本
# 雙擊此檔案即可自動在 Terminal 中啟動伺服器

# 切換到腳本所在的資料夾（stock 資料夾）
cd "$(dirname "$0")"

echo "========================================"
echo "  台灣股票分析工具 — 代理伺服器"
echo "========================================"
echo ""

# 確認 Python 版本
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "❌ 找不到 Python，請先安裝 Python 3"
    echo "   下載地址：https://www.python.org/downloads/"
    read -p "按 Enter 結束..."
    exit 1
fi

echo "✅ 使用 $($PY --version)"
echo ""

# 安裝 requests
echo "📦 確認 requests 套件..."
$PY -m pip install requests -q --break-system-packages 2>/dev/null || $PY -m pip install requests -q

echo ""
echo "🚀 啟動代理伺服器..."
echo ""
$PY stock_proxy.py
