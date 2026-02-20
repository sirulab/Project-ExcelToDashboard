# generate by ai
import pandas as pd
import random
from datetime import datetime, timedelta

# 設定要產生的筆數
NUM_ROWS = 100

# 1. 定義模擬資料庫
categories = ["電子零組件", "周邊設備", "網路設備", "軟體授權"]
products = {
    "電子零組件": ["電源供應器 650W", "8GB RAM", "1TB SSD"],
    "周邊設備": ["27吋螢幕", "機械式鍵盤", "無線滑鼠"],
    "網路設備": ["無線路由器", "交換器 8-port"],
    "軟體授權": ["Office 365", "防毒軟體"]
}
sales_reps = ["林小美", "陳大文", "張志明", "王阿明", "李春嬌"]

# 2. 隨機生成資料的函式
def generate_random_date(start_date="2024-01-01", end_date="2024-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

data = []

for _ in range(NUM_ROWS):
    category = random.choice(categories)
    product_name = random.choice(products[category])
    sales_rep = random.choice(sales_reps)
    
    # 隨機產生數量 (1~50) 與單價 (500~5000)
    quantity = random.randint(1, 50)
    unit_price = random.randint(5, 50) * 100 
    amount = quantity * unit_price
    
    order_date = generate_random_date()

    data.append({
        "訂單日期": order_date,           # Mapping: order_date
        "產品類別": category,             # Mapping: category
        "產品名稱": product_name,         # Mapping: product_name
        "業務負責人": sales_rep,          # Mapping: sales_rep
        "數量": quantity,                 # Mapping: quantity
        "未稅金額": amount                # Mapping: amount
    })

# 3. 直接轉成 DataFrame (修正點：移除 JSON 轉換)
df = pd.DataFrame(data)

# 存成 Excel
file_name = "sample_sales_data.xlsx"
df.to_excel(file_name, index=False)

print(f"✅ 成功生成測試檔案：{file_name}")
print(f"包含 {NUM_ROWS} 筆資料，欄位符合系統要求。")