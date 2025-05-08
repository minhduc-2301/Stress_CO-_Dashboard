import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Tải dữ liệu người dùng upload
uploaded_file = st.sidebar.file_uploader("📁 Tải lên file dữ liệu Excel", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("⚠️ Vui lòng tải lên file dữ liệu .xlsx để bắt đầu.")
    st.stop()

# Kiểm tra biến chính
stress_var = "Stress_CO2_Index_v2_auto_norm"
year_var = "year"
if stress_var not in df.columns or year_var not in df.columns:
    st.error(f"Dữ liệu thiếu cột '{stress_var}' hoặc '{year_var}'")
    st.stop()

# Phân loại mức độ stress
def classify_stress(value):
    if value <= 0.30:
        return "A – Cân bằng"
    elif value <= 0.60:
        return "B – Báo động"
    else:
        return "C – Mất cân bằng"

df["Stress_Level"] = df[stress_var].apply(classify_stress)

# Sidebar: chọn năm
selected_year = st.sidebar.selectbox("Chọn năm để xem chi tiết", df[year_var].unique())
row = df[df[year_var] == selected_year].iloc[0]
stress_value = row[stress_var]
stress_level = row["Stress_Level"]

# Sidebar: chọn nhóm DPSIR để xem biểu đồ phụ
selected_group = st.sidebar.selectbox("Chọn nhóm DPSIR để xem chi tiết", [
    "Drivers", "Pressures", "State", "Impacts", "Responses"
])
group_variables = {
    "Drivers": ["population", "gdp", "energy_per_capita", "energy_per_gdp", "fossil_share_energy"],
    "Pressures": ["co2", "co2_per_capita", "co2_per_gdp", "carbon_intensity_elec"],
    "State": ["temperature_change_from_co2", "total_ghg", "ghg_per_capita", "Stress_CO2_Index_v2_auto_norm"],
    "Impacts": ["temperature_change_from_ghg", "temperature_change_from_co2", "temperature_change_from_ch4"],
    "Responses": ["renewables_share_energy", "solar_share_energy", "wind_share_energy"]
}

# Tiêu đề
st.title("Dashboard Theo dõi Stress CO₂ chuẩn hóa")

# Biểu đồ chính Stress_CO2
st.subheader("Biểu đồ Stress CO₂ theo thời gian")
sns.set(style="white")
plt.figure(figsize=(10, 5))
palette = {"A – Cân bằng": "green", "B – Báo động": "orange", "C – Mất cân bằng": "red"}
for level in df["Stress_Level"].unique():
    subset = df[df["Stress_Level"] == level]
    plt.plot(subset[year_var], subset[stress_var], label=level, color=palette[level])
plt.xlabel("Năm")
plt.ylabel("Stress_CO₂ chuẩn hóa")
plt.legend(title="Mức độ căng thẳng")
plt.grid(False)
st.pyplot(plt)

# Biểu đồ phụ theo nhóm DPSIR
st.subheader(f"📈 Biểu đồ các biến trong nhóm {selected_group}")
variables = group_variables[selected_group]
fig, ax = plt.subplots(figsize=(10, 5))
for var in variables:
    if var in df.columns:
        ax.plot(df[year_var], df[var], label=var)
ax.set_xlabel("Năm")
ax.set_ylabel("Giá trị")
ax.legend()
ax.grid(False)
st.pyplot(fig)

# Thông tin chi tiết năm được chọn
st.subheader(f"Chi tiết năm {selected_year}")
st.metric("Chỉ số Stress CO₂ chuẩn hóa", f"{stress_value:.3f}", help="Stress_CO2_Index_v2_auto_norm")
st.info(f"Mức độ căng thẳng: **{stress_level}**")

# Cảnh báo
if stress_level == "C – Mất cân bằng":
    st.error("⚠️ Cảnh báo: Hệ sinh thái đang trong trạng thái quá tải nghiêm trọng.")
elif stress_level == "B – Báo động":
    st.warning("⚠️ Lưu ý: Căng thẳng môi trường đang tăng, cần giám sát và can thiệp.")
else:
    st.success("✅ Hệ sinh thái đang trong trạng thái cân bằng.")

# Hiển thị bảng phân cấp DPSIR có trọng số RF
st.subheader("📊 Hệ thống phân cấp DPSIR")
dpsir_data = {
    "Nhóm (Cấp A)": [
        "Drivers", "Drivers", "Drivers", "Drivers", "Drivers",
        "Pressures", "Pressures", "Pressures", "Pressures",
        "State", "State", "State", "State",
        "Impacts", "Impacts", "Impacts",
        "Responses", "Responses", "Responses"
    ],
    "Biến (Cấp B)": [
        "population", "gdp", "energy_per_capita", "energy_per_gdp", "fossil_share_energy",
        "co2", "co2_per_capita", "co2_per_gdp", "carbon_intensity_elec",
        "temperature_change_from_co2", "total_ghg", "ghg_per_capita", "Stress_CO2_Index_v2_auto_norm",
        "temperature_change_from_ghg", "temperature_change_from_co2", "temperature_change_from_ch4",
        "renewables_share_energy", "solar_share_energy", "wind_share_energy"
    ],
    "Trọng số (RF)": [
        0.0665, 0.0775, 0.0638, 0.0837, 0.0088,
        0.0591, 0.0591, 0.0494, 0.0507,
        0.0359, 0.0403, 0.0512, 0.0687,
        0.055, 0.0359, 0.0183,
        0.0156, 0.0441, 0.2115
    ]
}
dpsir_df = pd.DataFrame(dpsir_data)
st.dataframe(dpsir_df, use_container_width=True)

# Nút tải dữ liệu
st.download_button("📥 Tải dữ liệu đầy đủ", data=df.to_csv(index=False), file_name="stress_co2_data.csv")

st.caption("*Phân cấp theo khung DPSIR: Drivers – Pressures – State – Impacts – Responses*")
