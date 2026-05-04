# 台灣股票分析工具 Taiwan Stock Analyzer

輸入台股代號，即時查詢個股基本面、技術指標與財務數據的單頁分析工具。

**線上版本：** [tw-stock-analyzer-lac.vercel.app](https://tw-stock-analyzer-lac.vercel.app)

---

## 功能

- 即時股價、漲跌幅、成交量
- 技術指標：MA5 / MA20 / MA60、K 線圖
- 基本面數據：EPS、本益比、股價淨值比、殖利率
- 財務報表：營收、毛利率、營業利益率
- 法人買賣超、外資持股比例

## 專案結構

```
taiwan_stock_analyzer.html   # 前端主程式（單一 HTML 檔）
stock_proxy.py               # 本地 CORS 代理伺服器（Python）
啟動代理伺服器.bat            # Windows 一鍵啟動
啟動代理伺服器.command        # macOS 一鍵啟動
```

## 使用方式

### 線上版（Vercel）

直接開啟 [tw-stock-analyzer-lac.vercel.app](https://tw-stock-analyzer-lac.vercel.app)，輸入股票代號查詢。

### 本機執行

本機執行需要啟動代理伺服器，以解決瀏覽器 CORS 限制。

**1. 安裝依賴**

```bash
pip install requests
```

**2. 啟動代理伺服器**

- Windows：雙擊 `啟動代理伺服器.bat`，或執行：
  ```bash
  python stock_proxy.py
  ```
- macOS：雙擊 `啟動代理伺服器.command`

**3. 開啟前端**

保持代理伺服器視窗開啟，用瀏覽器開啟 `taiwan_stock_analyzer.html`。

> 按 `Ctrl+C` 可停止代理伺服器。

## 相關專案對照

本人另有一個 Streamlit 版本的股票分析工具 [stock-chart-analysis](https://github.com/caryhp2-cell/stock-chart-analysis)，兩者架構不同：

| | **tw-stock-analyzer（本專案）** | **stock-chart-analysis** |
|--|--|--|
| 框架 | 純 HTML + JS | Streamlit（Python）|
| 運作位置 | 瀏覽器端（Client-side） | 伺服器端（Server-side） |
| 資料來源 | TWSE / TPEx / FinMind | Yahoo Finance（yfinance）|
| 需要 Python server | 否 | 是 |
| 部署方式 | Vercel（靜態 CDN） | 本機執行 |
| 類比 | SPA（純前端） | SSR（Next.js Server-side） |

> 兩者都是「一個 URL 進去全搞定」，但運作原理不同。本專案因為不需要 server，所以能直接部署到 Vercel CDN；stock-chart-analysis 需要 Python server 持續運行，無法部署到 Vercel。

---

## 技術架構

- **前端：** 純 HTML / CSS / JavaScript + [Chart.js](https://www.chartjs.org/)
- **資料來源：**
  - [TWSE](https://www.twse.com.tw)（臺灣證券交易所）— 上市股票日K資料
  - [TPEx](https://www.tpex.org.tw)（證券櫃檯買賣中心）— 上櫃股票日K資料
  - [FinMind](https://finmindtrade.com)（FinMind API）— 財務報表、法人買賣超
- **部署：** Vercel（純靜態，三個資料來源均原生支援 CORS，不需要 proxy）
