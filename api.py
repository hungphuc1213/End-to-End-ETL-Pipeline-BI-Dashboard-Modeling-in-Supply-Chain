# api.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="HỆ THỐNG DỰ BÁO LỢI NHUẬN & CẢNH BÁO RỦI RO")

# Load models
profit_model = joblib.load("profit_model.pkl")
risk_model = joblib.load("risk_model_final.pkl")
profit_cols = joblib.load("profit_columns.pkl")
risk_cols = joblib.load("risk_columns.pkl")

class OrderInput(BaseModel):
    Order_Item_Quantity: int
    Order_Item_Discount_Rate: float
    Product_Price: float
    shipping_delay_days: int
    Type: str
    Market: str
    Category_Name: str
    Order_Region: str
    customer_total_orders: int = 1
    order_hour: int = 12
    is_weekend: int = 0

@app.post("/predict")
def predict_order(order: OrderInput):
    data = order.dict()
    
    # === DỰ BÁO LỢI NHUẬN ===
    df_profit = pd.DataFrame([data])
    df_p = pd.get_dummies(df_profit, drop_first=True)
    df_p = df_p.reindex(columns=profit_cols, fill_value=0)
    profit = profit_model.predict(df_p)[0]
    
    # === CẢNH BÁO RỦI RO ===
    df_risk = pd.DataFrame([data])
    df_r = pd.get_dummies(df_risk, drop_first=True)
    df_r = df_r.reindex(columns=risk_cols, fill_value=0)
    risk = risk_model.predict(df_r)[0]
    prob = risk_model.predict_proba(df_r)[0].max()
    
    # === RULE TỪ EDA ===
    alert = ""
    if data['Order_Item_Discount_Rate'] > 0.10:
        alert += "Discount >10% | "
    if data['Type'] in ['PAYMENT', 'TRANSFER']:
        alert += "Thanh toán online | "
    if data['shipping_delay_days'] > 5:
        alert += "Giao chậm | "
    
    return {
        "order_id": "NEW",
        "predicted_profit": round(float(profit), 2),
        "risk_level": risk,
        "confidence": f"{prob:.1%}",
        "alert": alert.strip(" | ") if alert else "An toàn",
        "action": "CẢNH BÁO NGAY" if risk == "High Risk" else "Theo dõi" if risk == "Medium Risk" else "Xử lý bình thường"
    }