# 更新 GitHub Pages 網站（正式發布版）

1. 下載新版 ZIP，右鍵選「解壓縮全部」。
2. 打開 GitHub 儲存庫：https://github.com/johnmantou-max/LLM-WIKI
3. 點選 `Add file` → `Upload files`。
4. 打開解壓縮後的專案**內部**，按 Ctrl+A 選取所有資料夾和檔案，直接拖曳至 GitHub 上傳區。**不要只傳 ZIP，也不要把整個外層專案資料夾再包一層**。
5. Commit changes。保留 `assets/`、`raw/`、`data/`、`wiki/`、`sources/`、`scripts/` 等目錄。若 GitHub 顯示同名檔案，請確認是更新而非另外建立嵌套資料夾。
6. 檢查網站：
   - https://johnmantou-max.github.io/LLM-WIKI/
   - https://johnmantou-max.github.io/LLM-WIKI/wiki.html
   - https://johnmantou-max.github.io/LLM-WIKI/graph.html
   - https://johnmantou-max.github.io/LLM-WIKI/deck.html
7. 頁面應顯示 **11 份來源摘要、10 篇學習筆記、11 張投影片**。
8. 本版 10 篇 Wiki 文章已由使用者確認為正式版；需更新全部同名 HTML 和相關檔案，使 GitHub Pages 同步顯示正式狀態。

GitHub Pages 只提供靜態 HTML、CSS 和 JS；需要 AI 重新整理文件時仍要在本機使用 Coding Agent。
