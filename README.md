# BTC Trading Wiki｜正式版

本專案依照先前確認的需求，採用 Karpathy 風格的來源導向 LLM Wiki，透過 Graph 與 Loop 分階段整理、驗證並產生 HTML Wiki、教學簡報及知識關聯圖。

## 本次增補

- 前五篇為使用者原先指定的公開網頁；後六篇依使用者明確授權「自己補齊需要的資料」，補充 SMC、Fed、CPI、美債殖利率、DXY、廣義美元指數資料。
- `raw/` 記錄 11 份繁體中文來源摘記，保留原文網址與小節標籤。不是網頁原文全文。
- `wiki/pages/` 收錄 10 篇可追溯摘要筆記，覆蓋六大領域。10 篇文章已由使用者確認為正式版，狀態均為 `approved`。
- `wiki/relations.json` 包含八條已核准的學習關聯；不代表已驗證市場因果。
- `deck.html` 是正式教學簡報；網頁與簡報均以 `assets/` 內的 CSS/JS 運作，上傳 GitHub 時請保留資料夾。
- 實作腳本：`scripts/ingest.py`、`scripts/build.py`、`scripts/check.py`。靜態檢查**不是**獨立 AI 語義審查。

## 網頁

- `index.html`：首頁
- `wiki.html`：學習知識庫與來源引用
- `graph.html`：知識關聯
- `deck.html`：教學簡報
- `workflow.html`：Graph / Loop 說明

## 引用與限制

來源以本站摘記 `[@SRC-...:p1:Lx-Ly]` 定位；精確到本地筆記行號，不是原文網頁全文行號。請透過原文 URL 和小節核對主張。尤其 SMC 與 BTC 宏觀因果，只能作為研究框架而非保證有效策略。

核准紀錄位於 `docs/manual-review.md`；執行報告位於 `reports/latest.md`。

**發布狀態：** 使用者確認正式發布（2026-11-23）。引用位置指本站來源摘要，非網頁原文行號。
