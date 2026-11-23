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

## GitHub Pages 部署

1. 建立儲存庫，例如 `btc-trading-wiki`。
2. 將 ZIP **解壓縮後的所有內容**放在儲存庫根目錄，確認 `index.html` 在根目錄。
3. 設定 Settings → Pages → Deploy from a branch → `main` / `(root)`。
4. 開啟 `/index.html`、`/wiki.html`、`/graph.html`、`/deck.html`、`/workflow.html` 測試。

此版網站會明確出現 `DRAFT / 待核准`，因為它是尚待人工審查的知識預覽。不要在課堂作業說明中將它稱為全部完成。

## 本機批次 ingest / 重新建置 / 品質檢查

```bash
python -m pip install -r requirements.txt
python scripts/ingest.py
python scripts/build.py
python scripts/check.py
```

- Python 3.10 以上；Markdown、TXT 不需額外套件，PDF 的文字抽取需安裝 pypdf。
- `build.py` 是靜態渲染工具，**不是自動執行的 AI Agent**。Graph + Loop 的語義修訂由 Coding Agent 與人工確認依 `AGENTS.md` 操作。
- `check.py` 主要做程式可驗證的來源數量、SHA-256、引用位置、內部連結與內容狀態；不能代替人工確認原文支持結論。
- **不得任意將 `status: draft` 改為 `approved`**；需真的閱讀原文驗收後才能簽核。

## 教師驗收注意

作業要求至少 ingest 5 篇資料，本專案的批次輸入為 5 份「經查閱網頁後自撰的來源摘記」，而非 5 份原網站全文。若老師要求**原始文章全文**作為 ingest 證據，這個差別必須在交件時說清楚；可合法取得原文並在新版本重新 ingest。重要議題的缺口也必須保留，不得添加無來源內容。
