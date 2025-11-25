import streamlit as st
import requests
import json

# ============================
# 🔧 1. THAY ĐƯỜNG DẪN API TẠI ĐÂY
# ============================
API_URL = "http://127.0.0.1:8000/predict"
# ============================

st.set_page_config(page_title="Cảnh báo Đơn hàng", layout="wide")
st.title("HỆ THỐNG DỰ BÁO LỢI NHUẬN & CẢNH BÁO RỦI RO")
st.markdown("**Nhập đơn hàng → Nhận cảnh báo trong 2 giây**")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Thông tin đơn hàng")
    quantity = st.number_input("Số lượng", 1, 100, 1)
    discount = st.slider("Giảm giá (%)", 0, 30, 10) / 100
    price = st.number_input("Giá sản phẩm ($)", 10, 10000, 500)
    delay = st.number_input("Ngày giao chậm", 0, 15, 0)
    payment = st.selectbox("Hình thức thanh toán", ["DEBIT", "CASH", "PAYMENT", "TRANSFER"])
    
with col2:
    market = st.selectbox("Thị trường", ["Pacific Asia", "Europe", "LATAM", "US"])
    region = st.text_input("Khu vực giao hàng", "Southeast Asia")
    category = st.text_input("Danh mục sản phẩm", "Cleats")
    customer_orders = st.number_input("Tổng đơn khách đã mua trước đó", 0, 1000, 1)

if st.button("DỰ ĐOÁN & CẢNH BÁO", type="primary"):
    payload = {
        "Order_Item_Quantity": quantity,
        "Order_Item_Discount_Rate": discount,
        "Product_Price": price,
        "shipping_delay_days": delay,
        "Type": payment,
        "Market": market,
        "Category_Name": category,
        "Order_Region": region,
        "customer_total_orders": customer_orders
    }

    # ============================
    # 🔍 2. KIỂM TRA API TRƯỚC KHI GỌI
    # ============================
    try:
        res = requests.post(API_URL, json=payload)
    except Exception as e:
        st.error(f"⚠️ Không thể kết nối API!\nKiểm tra API_URL hoặc API có đang chạy không.")
        st.info(f"API URL hiện tại: {API_URL}")
        st.stop()

    if res.status_code != 200:
        st.error(f"⚠️ API trả về lỗi {res.status_code}. Kiểm tra server FastAPI.")
        st.stop()

    response = res.json()

    # ============================
    # 📊 HIỂN THỊ KẾT QUẢ
    # ============================
    profit = response["predicted_profit"]
    risk = response["risk_level"]
    alert = response["alert"]
    action = response["action"]

    col1, col2 = st.columns(2)
    with col1:
        if profit > 0:
            st.success(f"LỢI NHUẬN DỰ BÁO: ${profit:,.0f}")
        else:
            st.error(f"LỖ DỰ BÁO: ${abs(profit):,.0f}")

    with col2:
        color = "red" if risk == "High Risk" else "orange" if risk == "Medium Risk" else "green"
        st.markdown(
            f"**MỨC RỦI RO:** <span style='color:{color}; font-size:24px'>{risk}</span>",
            unsafe_allow_html=True
        )
        st.warning(f"**Cảnh báo:** {alert}")
        st.info(f"**Hành động đề xuất:** {action}")
