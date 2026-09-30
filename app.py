import streamlit as st
import pandas as pd


# ==========================
# Cấu hình trang
# ==========================

st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)


# ==========================
# Hàm tính lãi
# ==========================

def tinh_lai_don(tien_gui, lai_suat, ky_han):
    """
    Lãi đơn:
    Lãi = Gốc * lãi suất năm * số năm
    """
    so_nam = ky_han / 12
    tien_lai = tien_gui * (lai_suat / 100) * so_nam
    
    return tien_lai



def tinh_lai_kep(tien_gui, lai_suat, ky_han, hinh_thuc):
    """
    Lãi kép theo kỳ nhập lãi
    """

    if hinh_thuc == "Lãnh lãi theo tháng":
        so_ky = ky_han
        lai_ky = lai_suat / 100 / 12

    elif hinh_thuc == "Lãnh lãi theo quý":
        so_ky = ky_han / 3
        lai_ky = lai_suat / 100 / 4

    else:
        so_ky = 1
        lai_ky = lai_suat / 100 * (ky_han / 12)


    tong_tien = tien_gui * (1 + lai_ky) ** so_ky

    tien_lai = tong_tien - tien_gui

    return tien_lai, tong_tien



def dinh_dang_tien(tien):
    return f"{tien:,.0f} VNĐ"



# ==========================
# Giao diện
# ==========================

st.title("💰 Ứng dụng tính lãi tiết kiệm")

st.write(
    "Tính toán tiền gửi ngân hàng theo phương pháp "
    "**lãi đơn hoặc lãi kép**."
)


# Nhập dữ liệu

tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=100000,
    value=10000000,
    step=100000
)


ky_han = st.number_input(
    "📅 Kỳ hạn gửi (tháng)",
    min_value=1,
    value=12,
    step=1
)


lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1
)


loai_lai = st.selectbox(
    "🔢 Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)


hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)



# ==========================
# Tính toán
# ==========================

if st.button("🧮 Tính lãi"):


    if loai_lai == "Lãi đơn":

        tong_lai = tinh_lai_don(
            tien_gui,
            lai_suat,
            ky_han
        )

        tong_tien = tien_gui + tong_lai


    else:

        tong_lai, tong_tien = tinh_lai_kep(
            tien_gui,
            lai_suat,
            ky_han,
            hinh_thuc
        )


    # Tính tiền lãi định kỳ

    if hinh_thuc == "Lãnh lãi theo tháng":

        so_ky = ky_han

    elif hinh_thuc == "Lãnh lãi theo quý":

        so_ky = ky_han / 3

    else:

        so_ky = 1


    lai_dinh_ky = tong_lai / so_ky



    # ==========================
    # Kết quả
    # ==========================

    st.divider()

    st.subheader("📊 Kết quả tính toán")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Tiền lãi định kỳ",
            dinh_dang_tien(lai_dinh_ky)
        )


    with col2:

        st.metric(
            "Tổng tiền lãi",
            dinh_dang_tien(tong_lai)
        )


    st.success(
        f"""
        💰 Tổng số tiền nhận được:

        **{dinh_dang_tien(tong_tien)}**
        """
    )


    # Bảng chi tiết

    st.subheader("📋 Chi tiết")


    data = {

        "Nội dung": [
            "Tiền gốc",
            "Tổng tiền lãi",
            "Tổng gốc + lãi",
            "Hình thức nhận lãi",
            "Phương pháp tính"
        ],

        "Giá trị": [

            dinh_dang_tien(tien_gui),

            dinh_dang_tien(tong_lai),

            dinh_dang_tien(tong_tien),

            hinh_thuc,

            loai_lai

        ]

    }


    df = pd.DataFrame(data)


    st.table(df)



# ==========================
# Công thức
# ==========================

with st.expander("📘 Công thức tính"):

    st.write(
        """
        **Lãi đơn**

        Lãi = Tiền gửi × Lãi suất năm × Số năm


        **Lãi kép**

        Tổng tiền = Gốc × (1 + lãi suất kỳ)^số kỳ


        Lưu ý:
        - Lãi suất nhập theo %/năm.
        - Lãi kép giả định tiền lãi được nhập vào gốc.
        """
    )
