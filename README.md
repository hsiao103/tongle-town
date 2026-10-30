# 主題閱讀鎮（v4，Sunnyside 風）

## 內容
- `index.html`：遊戲本體（單一檔案，素材已內嵌，可直接雙擊開啟或放到 GitHub Pages）
- `reading-sheet-apps-script.gs`：Google 試算表連動（成績寫入、題庫讀取）
- `reading-bank-題庫範本.csv`：4 個主題 × 20 題（基本／進階／高階），匯入試算表「題庫」分頁
- `assets/`：圖集（atlas.png／atlas.json）與打包腳本、題庫原始資料
- `CREDITS.txt`：素材來源與授權

## 玩法
搖桿／方向鍵／WASD 移動，A 鈕／空白鍵互動。10 個黃色地標答對拿徽章；梅花廣場旁 4 間藍色書屋（西遊記、小王子、木偶奇遇記、封神榜）每局隨機抽 10 題，選項位置隨機。
配分：基本 1／進階 2／高階 3（每局基本 4 題、進階 4 題、高階 2 題，滿分 18）。

## 連動 Google 試算表
1. 新增試算表，建立「成績」「題庫」兩個分頁；把 CSV 匯入「題庫」。
2. 擴充功能 → Apps Script，貼上 `reading-sheet-apps-script.gs`（可自訂 TOKEN）。
3. 部署 → 網頁應用程式（執行身分：我；存取權：所有人），複製 /exec 網址。
4. 遊戲網址加參數：`index.html?sheet=<exec網址>`（有 TOKEN 再加 `&token=暗號`）。
題庫分頁某主題至少 10 題時，會取代內建題庫；成績無網路時會暫存、下次補送。

## 可調整處（index.html 開頭 CONFIG）
PER_RUN（每局題數）、MIX（難度比例）、POINTS（配分）。
