#!/usr/bin/env python3
"""
台灣股票分析工具 — 本地代理伺服器 v1.1
============================================
解決瀏覽器 CORS 限制，代理 Yahoo Finance 財務資料。

【安裝依賴】
  pip install requests

【啟動方式】
  python stock_proxy.py

  啟動後請保持此視窗開啟，再用瀏覽器開啟 taiwan_stock_analyzer.html 即可。
  按 Ctrl+C 可停止伺服器。
"""

import json
import sys
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8765

YAHOO_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://finance.yahoo.com/",
    "Origin": "https://finance.yahoo.com",
}

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}


class ProxyHandler(BaseHTTPRequestHandler):

    # ── OPTIONS preflight ──────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()

    # ── GET ────────────────────────────────────────────────────────────
    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        qs     = parse_qs(parsed.query)

        # ── /health ────────────────────────────────────────────────────
        if path == "/health":
            self._json({"status": "ok", "port": PORT, "version": "1.1"})
            return

        # ── /api/yahoo/<TICKER> ────────────────────────────────────────
        if path.startswith("/api/yahoo/"):
            ticker  = path[len("/api/yahoo/"):]
            modules = qs.get(
                "modules",
                ["defaultKeyStatistics,financialData,summaryDetail,assetProfile"],
            )[0]

            # Try query1 first, then query2
            for host in ("query1", "query2"):
                url = (
                    f"https://{host}.finance.yahoo.com/v10/finance/quoteSummary/"
                    f"{ticker}?modules={modules}"
                )
                try:
                    r = requests.get(url, headers=YAHOO_HEADERS, timeout=15)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("quoteSummary", {}).get("result"):
                            print(f"  ✅ {ticker} 資料取得成功 ({host})")
                            self._json(data)
                            return
                except Exception as e:
                    print(f"  ⚠️  {host} 失敗: {e}")

            self._json({"error": "Yahoo Finance 無法取得資料，請稍後再試"}, status=502)
            return

        self._json({"error": "路徑不存在"}, status=404)

    # ── helper ─────────────────────────────────────────────────────────
    def _json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[代理] {self.client_address[0]}  {args[0]}  →  {args[1]}")


# ── 主程式 ──────────────────────────────────────────────────────────────
def main():
    # 確認 requests 已安裝
    try:
        import requests  # noqa: F401
    except ImportError:
        print("❌ 請先安裝 requests：pip install requests")
        sys.exit(1)

    server = HTTPServer(("localhost", PORT), ProxyHandler)

    print("=" * 52)
    print("  台灣股票分析工具 — 本地代理伺服器 v1.1")
    print("=" * 52)
    print(f"  ✅ 伺服器已啟動：http://localhost:{PORT}")
    print(f"  📂 請在瀏覽器開啟 taiwan_stock_analyzer.html")
    print(f"  ⛔ 按 Ctrl+C 停止伺服器")
    print("=" * 52)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止。")


if __name__ == "__main__":
    main()
