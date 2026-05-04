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

## 技術架構

- **前端：** 純 HTML / CSS / JavaScript + [Chart.js](https://www.chartjs.org/)
- **資料來源：** Yahoo Finance API
- **代理伺服器：** Python `http.server`（解決 CORS）
- **部署：** Vercel
