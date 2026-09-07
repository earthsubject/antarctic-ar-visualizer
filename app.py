import datetime
import streamlit as st

st.set_page_config(
    page_title="南極大氣長河 (AR) 查詢系統", page_icon="❄️", layout="centered"
)

st.title("❄️ 南極 IVT 時間軸互動查詢系統")
st.markdown("設定欲觀測的時間段，使用時間軸滑桿進行連續動態預覽。")

# 請改為您的 Hugging Face 帳號與專案名
HF_USERNAME = "您的帳號"
SPACE_NAME = "antarctic-ar-visualizer"
IMAGE_BASE_URL = f"https://huggingface.co/spaces/{HF_USERNAME}/{SPACE_NAME}/raw/main/plots/"

st.divider()

# 1. 選擇時間區間
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "起始日期",
        value=datetime.date(2015, 1, 19),
        min_value=datetime.date(2015, 1, 1),
        max_value=datetime.date(2015, 12, 31),
    )
with col2:
    end_date = st.date_input(
        "結束日期",
        value=datetime.date(2015, 1, 31),
        min_value=datetime.date(2015, 1, 1),
        max_value=datetime.date(2015, 12, 31),
    )

if start_date > end_date:
    st.error("錯誤：起始日期不能大於結束日期！")
else:
    # 2. 根據區間自動生成 6 小時間隔的時間序列清單
    time_list = []
    current_dt = datetime.datetime.combine(start_date, datetime.time(0, 0))
    end_dt = datetime.datetime.combine(end_date, datetime.time(18, 0))

    while current_dt <= end_dt:
        time_list.append(current_dt)
        current_dt += datetime.timedelta(hours=6)

    total_steps = len(time_list)

    st.subheader(f"📅 目前顯示區間：{start_date} 至 {end_date} (共 {total_steps} 個時間步)")

    # 3. 時間軸滑桿 (Slider)
    selected_idx = st.slider(
        "拖曳滑桿切換時間點：",
        min_value=0,
        max_value=total_steps - 1,
        value=0,
        format="",
    )

    # 4. 取得當前滑桿對應的時間點與圖片網址
    target_dt = time_list[selected_idx]
    dt_str = target_dt.strftime("%Y-%m-%d_%H-%M")
    file_name = f"IVT_{dt_str}.png"
    image_url = f"{IMAGE_BASE_URL}{file_name}"

    st.markdown(
        f"#### 🕒 當前時間：**{target_dt.strftime('%Y-%m-%d %H:%M')} UTC**"
    )

    # 5. 渲染圖片
    with st.spinner("讀取氣象圖中..."):
        try:
            st.image(
                image_url,
                caption=f"Antarctic IVT - {target_dt.strftime('%Y-%m-%d %H:%M')} UTC",
                use_column_width=True,
            )
        except Exception:
            st.warning(f"尚未尋獲該時間點圖片 ({file_name})，請確認是否已上傳。")

with st.expander("ℹ️ 系統操作說明"):
    st.write(
        """
    1. 在上方選擇關注的日期區間。
    2. 拖曳中間的「時間軸滑桿」，即可快速查看連續的水氣輸送 (IVT) 演變情況。
    3. 數據來源為 ECMWF ERA5 再分析資料。
    """
    )
