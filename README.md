# tpex500 每日更新 — 改為 GitHub Actions 版（免裝置、免外流 PAT）

## 這個改動做了什麼

把原本「Claude 排程 → 連你的電腦 → 用明文存在排程訊息裡的 GitHub PAT 執行 git push」的流程，
整個搬進這個 repo 自己的 GitHub Actions，變成：

- 不需要你的電腦開機、不需要裝置綁定。
- 不需要任何個人 PAT。Actions 用 GitHub 自動核發、隨 job 結束即失效的內建
  `GITHUB_TOKEN`，只在這個 repo 內有寫入權限，範圍最小。
- 股價抓取從「呼叫 WebFetch 讓 LLM 讀網頁擷取數字」改成直接呼叫
  FinMind 與 Yahoo Finance 的 JSON API（`scripts/fetch_prices.py`），純程式化、
  可在 Actions runner 上穩定執行，不再需要 30–40 分鐘的人工介入式抓取。
- `merge500.py` / `build_html_500.py` / `build_xlsx_500.py` 三支腳本邏輯完全比照原本手冊，
  未更動任何欄位計算或版面邏輯。

## 安裝步驟（一次性，需要你手動做）

1. 把這個資料夾的內容複製進 `yanhsu/tpex500` repo 的**預設分支**（例如 `main`）：
   - `.github/workflows/daily-refresh.yml`
   - `data/seed500.txt`
   - `scripts/fetch_prices.py`
   - `scripts/merge500.py`
   - `scripts/build_html_500.py`
   - `scripts/build_xlsx_500.py`

   `gh-pages` 分支不用動，workflow 會自動 checkout 它、把新的
   `index.html` / `taiwan_stocks_top500.xlsx` 覆蓋進去再 push。

2. 到 repo 的 **Settings → Actions → General → Workflow permissions**，
   確認選的是「**Read and write permissions**」（預設可能是唯讀，這樣
   `GITHUB_TOKEN` 才有權限 push 到 `gh-pages`）。

3. Commit + push 這些檔案後，先手動觸發一次測試：
   到 repo 的 **Actions** 分頁 → 選 `Daily refresh (price / yield)` →
   `Run workflow`，看 log 確認：
   - `fetch_prices.py` 有成功抓到大部分代號的股價（少數抓不到會自動用
     `seed500.txt` 裡的備用價，這是正常設計，不是錯誤）。
   - 最後一步有正常 commit/push，或顯示「nothing to commit」（股價跟昨天
     完全一樣時的正常結果）。

   ⚠️ 我這邊（雲端 sandbox）的網路是白名單制，連不到
   `api.finmindtrade.com` 和 `query1.finance.yahoo.com`，所以
   `fetch_prices.py` 的 API 呼叫邏輯**沒辦法在我這裡實際跑一次驗證**，
   只做了語法檢查與邏輯比對（跟手冊原本描述的 FinMind/Yahoo 規則一致）。
   GitHub Actions runner 是完整對外連線，理論上沒問題，但你手動觸發那一次
   務必看一下 log 確認真的有抓到價格，而不是全部靠 seed 備用值。

4. 排程時間目前設定成每天 UTC 10:10（= 台北時間 18:10），對應原本手冊
   「時間 ≥ 18:00 才建檔」的邏輯。要改時間就改
   `.github/workflows/daily-refresh.yml` 裡的 `cron` 那行。

## 收尾：舊憑證與舊排程建議處理

- 舊的那組 `github_pat_...`（存在 trigger
  `trig_01JnWSmN2Q9RipLnvLM4ybC3` 的訊息內容裡）建議直接去 GitHub
  Settings → Developer settings → Personal access tokens 撤銷掉，不用再留著。
- 這兩個舊的 Claude 排程（`台股500大 每小時更新（裝置綁定版）` 與
  `台股前500大 每日股價/殖利率更新並推送GitHub Pages`）在確認新的
  Actions 版跑穩之後，可以停用或刪除，避免兩邊同時各自 push 造成衝突。
