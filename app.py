import datetime
import streamlit as st

st.set_page_config(
    page_title="南極大氣長河 (AR) 查詢系統", page_icon="❄️", layout="centered"
)

st.title("❄️ 南極 Integrated Vapor Transport (IVT) 查詢系統")
st.markdown(
    "本系統提供 2015 年 ERA5 南極地區水氣輸送量 (IVT) 與大氣長河觀測預覽。"
)

st.divider()

col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input(
        "選擇日期",
        value=datetime.date(2015, 1, 19),
        min_value=datetime.date(2015, 1, 1),
        max_value=datetime.date(2015, 12, 31),
    )

with col2:
    selected_time = st.selectbox(
        "選擇 UTC 時間", options=["00:00", "06:00", "12:00", "18:00"], index=0
    )

date_str = selected_date.strftime("%Y-%m-%d")
time_str = selected_time.replace(":", "-") + "-00"
file_name = f"IVT_{date_str}_{time_str}.png"

# 請替換為您儲存圖片的公開 URL 基底
IMAGE_BASE_URL = "https://your-storage-domain.com/AR_Antarctica_Plots/"
image_url = f"{IMAGE_BASE_URL}{file_name}"

st.divider()
st.subheader(f"📅 查詢時間：{date_str} {selected_time} (UTC)")

with st.spinner("正在讀取極地氣象圖..."):
    try:
        st.image(
            image_url,
            caption=f"Antarctic IVT Distribution - {date_str} {selected_time}",
            use_column_width=True,
        )
    except Exception:
        st.error(
            "無法載入圖片，請確認該時間點是否有輸出資料或圖片 URL 是否正確。"
        )

with st.expander("ℹ️ 關於數據與說明"):
    st.write(
        """
    - **數據來源**：ECMWF ERA5 Reanalysis
    - **投影方式**：South Polar Stereographic (-50°S 至 -90°S)
    - **變數定義**：Integrated Vapor Transport ($IVT = \\sqrt{viwve^2 + viwvn^2}$)
    """
    )
