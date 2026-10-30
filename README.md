# 圖片作品庫 · Image Library

持續累積的圖片作品庫：海報、圖解、教學插圖。每件作品放在獨立資料夾，原件可下載列印。

- 線上瀏覽：<https://tyhcch1234.github.io/image/>
- 已收錄：正向教育海報系列（4 張 16:9）

## 目錄結構

```
collections/
  positive-education-posters/     ← 一個系列一個資料夾
    01_性格強項_24種力量_16x9.png
    ...
    正向教育海報_四張_16x9.pdf
    meta.json                     ← 標題、描述、PDF
    thumbs/                       ← 自動產生的縮圖
data/images.json                  ← 自動產生的清單（網頁讀取）
index.html                        ← 作品庫首頁（GitHub Pages）
tools/build_manifest.py           ← 重建縮圖 + 清單
```

## 新增一個系列

1. 建立 `collections/<系列名稱>/`，把圖片放進去（png / jpg / webp）。
2. 在該資料夾寫 `meta.json`：

```json
{
  "title": "系列名稱",
  "subtitle": "English subtitle",
  "date": "2026-10-30",
  "desc": "一兩句介紹。",
  "titles": { "檔名.png": "卡片上顯示的標題" },
  "pdf": "合集.pdf",
  "pdf_label": "合集 PDF（可直接列印）"
}
```

3. 重建縮圖與清單：

```bash
python3 tools/build_manifest.py
```

4. 提交：

```bash
git add -A && git commit -m "add: 新系列" && git push
```

`meta.json` 全部欄位都是選填；沒有 `titles` 時會用檔名當標題，沒有 `pdf` 就不顯示 PDF 按鈕。
