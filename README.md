# Project-ExcelToDashboard

Project-ExcelToDashboard 是一個輕量級的數據自動化與視覺化儀表板系統。
借鑑了自動化資料處理的流暢體驗，此專案旨在提供企業或個人一個無縫的銷售數據轉換流程：
從上傳原始 Excel 銷售報表、自動清理與正規化資料，到寫入資料庫，並最終在網頁儀表板上呈現互動式的視覺化圖表。

### 核心功能

* **檔案上傳與自動解析**：支援透過網頁表單上傳 Excel 檔案，並自動對應並清洗欄位（如訂單日期、產品類別、業務負責人、金額等）。
* **資料庫管理**：自動清除舊有資料，將最新清洗後的銷售紀錄 (`SalesRecord`) 安全地寫入資料庫進行持久化保存。
* **動態數據視覺化**：整合 Plotly 引擎自動聚合數據，產生互動式的每日銷售線圖或各類別銷售排行長條圖。
* **直覺的儀表板**：提供簡潔的 Web 介面，讓使用者可隨時查看圖表，並支援多種資料分組維度（如依日期、類別、業務員等）的快速切換。

### 技術棧

* **後端**：Python 3.13+, FastAPI
* **資料處理與視覺化**：Pandas, Plotly, openpyxl
* **資料庫 ORM**：SQLModel (`database.py` & `models.py`)
* **前端渲染**：Jinja2 Templates (`html/`)

### 資料表模型

本專案採用關聯式資料庫設計來儲存標準化後的數據，目前僅定義根據模板excel的欄位：
包含 `order_date`, `category`, `sales_rep`, `product_name`, `quantity`, `amount`

### 資料夾結構

```text
Project-ExcelToDashboard/
├── database.py       # 資料庫連線與設定
├── generate_data.py  # 測試資料生成腳本
├── models.py         # SQLModel 資料表模型
├── requirements.txt  # Python 套件清單
├── main.py           # 系統進入點 (Entry point)
└── html/             # 網頁樣板目錄
    └── dashboard.html# 儀表板前端網頁視圖

```


### 本地端開發設定

請依照以下步驟在本地環境中運行本專案：

### 1. 複製專案與建立虛擬環境

```
git clone https://github.com/sirulab/Project-ExcelToDashboard.git
cd Project-LINKER
python -m venv venv

# 啟動虛擬環境 (Windows)
venv\Scripts\activate
```

### 2. 安裝依賴套件

```
pip install -r requirements.txt
```

### 3. 啟動伺服器

```
python src/main.py
```
