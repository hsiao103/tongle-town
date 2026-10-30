/**
 * 主題閱讀鎮 — Google 試算表連動（Apps Script）
 * 1. 開一份新的 Google 試算表，建立兩個工作表：「成績」「題庫」
 * 2. 「題庫」第 1 列貼上標題：主題,難度,題目,正確答案,錯誤答案1,錯誤答案2,錯誤答案3,解析
 *    （可把 reading-bank-題庫範本.csv 整份匯入；老師改題目、加題目都在這裡）
 * 3. 試算表選單：擴充功能 → Apps Script，貼上本檔，儲存
 * 4. 部署 → 新增部署作業 → 類型「網頁應用程式」→ 執行身分「我」→ 存取權「所有人」→ 複製 /exec 網址
 * 5. 遊戲網址後面加：?sheet=<網址>（有設 TOKEN 時再加 &token=暗號）
 */
const TOKEN = '';                 // 選填：自訂暗號，遊戲網址要帶相同的 &token=
const SCORE_SHEET = '成績';
const BANK_SHEET = '題庫';

function doPost(e) {
  try {
    const p = JSON.parse(e.postData.contents);
    if (TOKEN && p.token !== TOKEN) return out_('forbidden');
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sh = ss.getSheetByName(SCORE_SHEET) || ss.insertSheet(SCORE_SHEET);
    if (sh.getLastRow() === 0) {
      sh.appendRow(['時間', '班級', '姓名', '主題', '得分', '滿分', '百分比', '基本', '進階', '高階', '用時(秒)', '評等']);
      sh.setFrozenRows(1);
    }
    const t = new Date(p.time);
    sh.appendRow([t, p.cls, p.name, p.theme, p.score, p.max, p.pct / 100, p.basic, p.advanced, p.high, p.seconds, p.rank]);
    sh.getRange(sh.getLastRow(), 7).setNumberFormat('0%');
    return out_('ok');
  } catch (err) {
    return out_('error: ' + err);
  }
}

// 遊戲開始時讀取題庫：?action=bank → 回傳「題庫」工作表的 CSV
function doGet(e) {
  if (e && e.parameter && e.parameter.action === 'bank') {
    const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(BANK_SHEET);
    if (!sh) return out_('');
    const csv = sh.getDataRange().getDisplayValues()
      .map(r => r.map(c => '"' + String(c).replace(/"/g, '""') + '"').join(',')).join('\n');
    return ContentService.createTextOutput(csv).setMimeType(ContentService.MimeType.CSV);
  }
  return out_('主題閱讀鎮 API 運作中');
}

function out_(s) { return ContentService.createTextOutput(s); }
