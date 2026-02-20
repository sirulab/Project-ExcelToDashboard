from database import get_session, create_db_and_tables
from sqlmodel import Session, select
import models

from typing import Annotated, List, Dict
import uuid
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import io
import pandas as pd
import plotly.express as px


app = FastAPI()
templates = Jinja2Templates(directory="html")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

db_dependency = Annotated[Session, Depends(get_session)]

def generate_chart_html(df: pd.DataFrame, group_by: str):
    if df.empty:
        return None
    
    # 日期格式
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'])

    # 聚合計算
    if group_by == "order_date":
        df_grouped = df.groupby("order_date")["amount"].sum().reset_index().sort_values("order_date")
        fig = px.line(df_grouped, x="order_date", y="amount", title="每日銷售", markers=True)
    elif group_by in df.columns:
        df_grouped = df.groupby(group_by)["amount"].sum().reset_index().sort_values("amount", ascending=False)
        fig = px.bar(df_grouped, x=group_by, y="amount", title=f"銷售排行 ({group_by})")
    else:
        return None

    # 設定圖表樣式
    fig.update_layout(height=500, margin=dict(t=50, l=20, r=20, b=50))
    # 轉成 HTML div 字串(plotly)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

COLUMN_MAPPING = {
    "order_date": ["訂單日期", "日期", "Date"],
    "category": ["產品類別", "類別", "Category"],
    "sales_rep": ["業務負責人", "業務", "Salesperson"],
    "product_name": ["產品名稱", "品名", "Product"],
    "quantity": ["數量", "Qty"],
    "amount": ["未稅金額", "金額", "Amount"]
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed_map = {}
    for col in df.columns:
        col_clean = str(col).strip()
        for db_field, aliases in COLUMN_MAPPING.items():
            if col_clean in aliases:
                renamed_map[col] = db_field
                break
    if not renamed_map:
        raise ValueError("無法識別欄位")
    df = df.rename(columns=renamed_map)
    return df[[c for c in df.columns if c in COLUMN_MAPPING.keys()]]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: db_dependency, group_by: str = "order_date"):
    # 讀取資料庫
    statement = select(models.SalesRecord)
    df = pd.read_sql(statement, db.bind)
    
    # 產生圖表
    chart_html = generate_chart_html(df, group_by)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "chart_html": chart_html,
        "current_group": group_by
    })

# 2. 上傳 (POST): 處理檔案 -> 存 DB -> 重新渲染頁面
@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, db: db_dependency, file: UploadFile = Form(...)):
    message = ""
    chart_html = None
    
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        df = normalize_columns(df)
        
        # 資料清洗與寫入
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df = df.dropna(subset=['order_date', 'amount'])
        
        records = df.to_dict(orient='records')
        db.exec(models.SalesRecord.__table__.delete())
        for record in records:
            if pd.isna(record.get('quantity')): record['quantity'] = 0
            db.add(models.SalesRecord(**record))
        db.commit()
        
        message = f"成功匯入 {len(records)} 筆資料！"
        
        # 匯入後直接產生預設圖表
        chart_html = generate_chart_html(df, "order_date")

    except Exception as e:
        message = f"錯誤：{str(e)}"
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "message": message,
        "chart_html": chart_html,
        "current_group": "order_date"
    })