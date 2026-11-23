# 第十週作業｜BTC Trading Wiki（正式發布，待網站操作驗收）

> 使用者已於 2026-11-23 確認正式發布。程式靜態檢查通過；仍需瀏覽器操作測試。

## 1. Wiki 主題與介紹

這次建立「BTC Trading Wiki」，先經過十題需求訪談，選擇個人學習型、深入理解、精確引用、衝突並列、批次 ingest 和 Graph + Loop 工作流程。六大領域是比特幣基礎、技術分析、SMC、永續合約、總體經濟和風險管理。

## 2. Wiki 連結或成果

- Wiki： https://johnmantou-max.github.io/LLM-WIKI/wiki.html
- 已 ingest：11 份來源摘要（使用者指定 5 篇 + 授權 AI 補充 6 篇），原網址登錄於 `sources/manifest.json`。
- 知識筆記：10 篇 `wiki/pages/`，全部為 `approved`，使用者已確認正式發布。引用 p1:Lx 是本站中文摘要的定位，非原文網頁頁碼。
- 關聯圖：https://johnmantou-max.github.io/LLM-WIKI/graph.html

## 3. HTML 教學簡報

- https://johnmantou-max.github.io/LLM-WIKI/deck.html
- 11 頁來源導向的教學簡報。原先被要求刪除的「Graph + Loop 與後續驗收」不再出現。

## 4. Graph / Loop 設計

Graph：指定或授權來源 → 批次匯入及定位 → 來源證據卡 → Wiki 文章 → 程式檢查 → 人工確認 → 產出網頁／簡報 → 再檢查 → 交付。

Loop：每個節點內「產生 → 驗證 → 只修錯誤 → 重檢」，最多三輪；不足或達上限就停止、留下報告。

## 5. 執行與檢查紀錄

- `scripts/ingest.py`：註冊 11 份不同來源摘要，沒有抽取失敗。
- `scripts/build.py`：產生首頁、Wiki、關聯圖、流程頁與 11 頁教學簡報。
- `scripts/check.py`：結構、SHA-256、筆記行號、HTML 路徑與關聯來源 ID 檢查通過；使用者人工核准已登錄。詳情見 `reports/latest.md`。
- 瀏覽器自動化在本環境受限制，仍須部署後驗證搜尋、連結、簡報控制及手機排版。

## 6. 反思（請依親自檢查後補寫）

起初只有五篇來源，雖然達到 ingest 數量，卻沒有完整涵蓋 SMC 和總體經濟。第一次檢查發現這個缺口後，我新增六個有原始網址、明確章節的來源摘要，而不是要求 AI 憑記憶補齊。SMC 描述的是交易者使用的價格分析框架，宏觀資料則提供制度與數據定義；兩者都不應被說成 BTC 的保證交易訊號。後續仍可改善的是原文語義細部核對與獨立 AI 審查，避免程式檢查通過就誤以為內容可靠。
