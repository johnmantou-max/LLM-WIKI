# 實際網頁功能檢查（2026-11-23）

## 執行方式

使用 Chromium 無頭瀏覽器，將生成的 HTML、CSS、JavaScript 嵌入測試頁面，**不依賴網路連線**。瀏覽器環境禁止直接開啟 `file://` 與本機 HTTP URL，因此測試為等效 HTML/CSS/JS 內容載入，尚未測試真實 GitHub Pages 部署。

## 結果

- `index.html`、`wiki.html`、`graph.html`、`deck.html` 均能成功渲染；沒有 JavaScript page error。
- Wiki 搜尋輸入 `MACD` 後可找到 1 篇相關文章。
- 知識關聯頁的 SVG 分類與草稿文章節點可以正常渲染並包含連結。
- 教學簡報共 9 頁；按「下一頁」後頁碼從 1/9 變成 2/9。
- 390px 手機視窗：Wiki 與簡報均沒有水平超出（scrollWidth = 390px）。
- 截圖保存在 `docs/preview-*.png`。

## 尚待人工測試

- 推送 GitHub Pages 後逐頁查看實際網址。
- 逐篇原網頁與摘要語義比對，並依 `docs/manual-review.md` 人工簽核。
- 涵蓋 SMC 與總體經濟的額外來源仍未提供。
