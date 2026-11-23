# BTC Trading Wiki — Append-only Log

## [2026-11-23] init | requirement-confirmed
- 需求：十題訪談已確認，使用者要求建立 AGENTS.md 與專案。
- 動作：建立空 Wiki 與工作流程；沒有匯入任何使用者原始文章。
- 狀態：待使用者放入 raw/ 並執行批次 ingest。

## [2026-11-23] ingest | batch scan
- 來源：0 篇；解析錯誤：0；完全重複：0；5 篇門檻：未達標。
- 詳情：docs/import-report.md、data/source_index.json；此處不代表 AI 語義審查已執行。

## [2026-11-23] ingest | batch scan
- 來源：5 篇；解析錯誤：0；完全重複：0；5 篇門檻：達標。
- 詳情：docs/import-report.md、data/source_index.json；此處不代表 AI 語義審查已執行。

## [2026-11-23] ingest | user-selected five public articles
- 使用者明確選定先前列出的 5 個網頁作為知識來源。已逐頁查閱，將精簡的中文摘要與「原文章節」記入 raw/；未下載或儲存任何原文全文。
- 執行 scripts/ingest.py：5 篇不同來源筆記，SHA-256 與行號均可追溯。
- 產生 6 篇 draft Wiki，**未經人工核准，未執行獨立 AI 語義審查**。
- 發現資料缺口：SMC、總體經濟無直接來源；保留未完成狀態。

## [2026-11-23] lint + browser | draft preview
- 5 份來源摘記通過解析，6 篇 draft 的引用格式與位置完成腳本驗證。
- 靜態檢查：243/248 PASS；五項 BLOCKER 未過（正式核准與六領域證據不足）。
- Chromium 靜態內容載入：桌機 Wiki 搜尋 MACD 正常、簡報 9 頁切換正常、手機無水平溢出。
- 無獨立 AI 語義審查與使用者簽核，不得宣稱正式完成。

## [2026-11-23] ingest | batch scan
- 來源：11 篇；解析錯誤：0；完全重複：0；5 篇門檻：達標。
- 詳情：docs/import-report.md、data/source_index.json；此處不代表 AI 語義審查已執行。

## [2026-11-23] source expansion / wiki draft
- 因使用者授權自行補齊資料，新增六份獨立公開來源的中文摘記：SMC (TradingView/LuxAlgo)、FOMC (Fed)、CPI (BLS)、DGS10 (FRED)、DXY (ICE)、DTWEXBGS (FRED)。
- 批次 ingest 11 份來源摘要。新增四篇草稿文章，補齊六大主題的教學筆記；更新八條來源導向關聯提案。
- 引用的 p1:Lx 僅定位本站摘記，不代表原文全文精確行號；語義審查與人工核准尚未完成。

- 2026-11-23：使用者已確認內容可正式發布；10 篇 Wiki 文章與 8 條學習關聯狀態改為 `approved`。
