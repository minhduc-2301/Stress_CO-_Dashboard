# 🌍 Stress CO₂ Dashboard – Việt Nam (DPSIR Framework)

Một dashboard Streamlit trực quan giúp theo dõi và đánh giá chỉ số Stress_CO₂ chuẩn hóa theo mô hình DPSIR (Drivers – Pressures – State – Impacts – Responses).

## 🚀 Tính năng

- Tải dữ liệu `.xlsx` ngay trên giao diện web
- Phân loại chỉ số Stress_CO₂ theo thang A–B–C
- Biểu đồ theo năm + biểu đồ phụ theo từng nhóm DPSIR
- Bảng phân cấp biến DPSIR với trọng số từ mô hình Random Forest
- Cho phép tải toàn bộ dữ liệu đã phân tích

## 📦 Cách sử dụng trên Streamlit Cloud

1. Tạo repo GitHub (ví dụ: `stress-co2-dashboard`)
2. Upload 2 file:
   - `app.py` (code Streamlit)
   - `README.md` (file này)
3. Truy cập [Streamlit Cloud](https://streamlit.io/cloud)
4. Bấm **New app**, kết nối GitHub
5. Chọn repo + file `app.py`, bấm **Deploy**
6. Chia sẻ link công khai cho mọi người sử dụng!

## 📁 Cấu trúc dữ liệu đầu vào

File Excel `.xlsx` cần có ít nhất 2 cột bắt buộc:

- `year`: năm quan sát
- `Stress_CO2_Index_v2_auto_norm`: chỉ số Stress CO₂ chuẩn hóa

Và các biến khác tương ứng với khung DPSIR như: `population`, `gdp`, `co2`, `renewables_share_energy`, v.v.

## 📬 Liên hệ & Đóng góp

Pull request hoặc góp ý vui lòng gửi về GitHub repo hoặc qua email.