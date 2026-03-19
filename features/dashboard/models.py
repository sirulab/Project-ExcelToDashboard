# models.py
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date

class SalesRecord(SQLModel, table=True):
    __tablename__ = "sales_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    order_date: date = Field(index=True)      # 日期
    category: str = Field(index=True)         # 產品類別
    sales_rep: str = Field(index=True)        # 業務負責人
    product_name: str                         # 產品名稱
    quantity: int                             # 數量
    amount: float                             # 金額