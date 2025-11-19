@echo off
echo ========================================
echo   CHẠY HỆ THỐNG DỰ BÁO & CẢNH BÁO RỦI RO
echo   (C) 2025 - Dự án của bạn
echo ========================================
echo.
echo [1] Đang khởi động API (FastAPI)...
start "API - DỰ BÁO LỢI NHUẬN" cmd /c "python -m uvicorn api:app --reload"

timeout /t 4 >nul
echo [2] Đang mở Dashboard (Streamlit)...
start "DASHBOARD QUẢN LÝ" cmd /c "python -m streamlit run app.py"

echo.
echo XONG! Đã mở 2 cửa sổ:
echo   - API: http://127.0.0.1:8000/docs
echo   - Dashboard: http://127.0.0.1:8501
echo.
pause