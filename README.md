# BTC Trading Wiki｜五篇使用者指定來源版

依照使用者已確認的十項需求，採用 Karpathy 風格的 LLM Wiki、Graph + Loop、五篇文章來源與 GitHub Pages 靜態展示。

## 本輪成果與真實狀態

- ✅ 已核對使用者選定的 **5 篇公開網頁**（Bitcoin.org、TradingView、Coinbase、Binance Academy×2）。
- ✅ 將這五篇網頁的**精簡中文重點摘記**置於 `raw/`，執行批次 `ingest.py`，取得 5 個 SHA-256 及位置化文字。
- ✅ 撰寫 **6 篇 Markdown Wiki 草稿**，保留來源 ID，並可以在 `wiki.html` 搜尋、分類與查看完整內容。
- ✅ 生成可瀏覽的 **9 頁 HTML 教學簡報草稿**，以及 Graph / Loop 說明與知識關聯預覽。
- ⬜ Wiki 6 篇仍為 `draft`，未經使用者人工核准，也未經獨立對話的 AI 內容審查。
- ⬜ 五篇原文未全文收錄；本站儲存的是自撰摘記與原網址、原文章節。**不能宣稱已匯入五篇原始文章全文。**
- ⬜ 五篇文章目前不足以支持兩項已規劃領域：**SMC（OB／FVG）**與**總體經濟（Fed／CPI／DXY）**，故沒有憑空編造這些領域的知識文。

## 專案檔案

| 路徑 | 功能 |
|---|---|
| `AGENTS.md` | 需求與資料邊界、Graph/Loop、引用及停止條件 |
| `raw/01-05*.md` | 五份指定原文章節的繁中摘要，非原文全文 |
| `sources/manifest.json` | 網址、機構、更新日期與資料性質 |
| `data/source_index.json` | SHA-256、摘記行號、來源 ID |
| `data/extracted/` | 具 `p1:Lx` 定位的本站摘要 |
| `wiki/pages/` | 六篇含精確本地註記的 draft 文章 |
| `wiki/index.md`, `wiki/log.md` | Wiki 索引與處理過程 |
| `index.html`, `wiki.html`, `graph.html`, `deck.html`, `workflow.html` | 可用 GitHub Pages 開啟的網頁 |
| `docs/import-report.md` | 批次匯入證明 |
| `reports/latest.md` | 靜態檢查及未通過關卡 |
