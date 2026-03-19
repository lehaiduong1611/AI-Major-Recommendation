import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 0. MOCK LOGIC (Giả lập logic AI để hiển thị) ---
def mock_generate_explanation(gpa_dict, holland_dict, major_name):
    # Logic giả lập lấy ra 1 môn/tính cách cao nhất
    top_h = max(holland_dict, key=holland_dict.get)
    top_s = max(gpa_dict, key=gpa_dict.get)
    
    explanation = f"**I. Cơ sở Tâm lý học:** Dựa trên dữ liệu, hệ thống nhận thấy chỉ số **{top_h.replace('Holland_', '')}** của bạn rất nổi trội... Phù hợp xuất sắc tố chất của ngành {major_name}.\n\n**II. Cơ sở Học thuật:** Mức điểm **{top_s} ({gpa_dict[top_s]})** là một chỉ số ưu tú..."
    return explanation

@st.cache_data
def mock_load_university_data():
    # Tạo dữ liệu Excel giả lập
    majors = ['CƠ ĐIỆN TỬ', 'KỸ THUẬT PHẦN MỀM', 'THIẾT KẾ ĐỒ HỌA']
    data = []
    schools = {
        'Top': ['FPT University (Hà Nội)', 'Đại học Bách Khoa', 'Đại học CNTT'],
        'Mid': ['Đại học Công nghiệp', 'Đại học Giao thông', 'Đại học FPT (Đà Nẵng)'],
        'Safe': ['Đại học Công nghệ Sài Gòn', 'Cao đẳng FPT', 'Đại học Văn Lang']
    }
    for m in majors:
        for p, s_list in schools.items():
            for s in s_list:
                score = 27.5 if p == 'Top' else 24.0 if p == 'Mid' else 19.5
                data.append({
                    'Nganh_Hoc': m,
                    'Ten_Truong': s,
                    'To_Hop_Mon': 'A00, A01',
                    'Diem_Chuan': score,
                    'Phan_Loai_Truong': p
                })
    return pd.DataFrame(data)

# --- 1. CẤU HÌNH GIAO DIỆN & CSS TỐI GIẢN ---
st.set_page_config(page_title="AI Recommendation System - UI Demo", layout="wide")

custom_css = """
<style>
    /* Tổng thể nền tảng trắng sạch */
    .stApp {
        background-color: #fdfdfc;
        color: #2b2b2b;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Thiết kế Sidebar chuyên nghiệp tông Navy */
    [data-testid="stSidebar"] {
        background-color: #1a2942;
        color: #f1f3f5;
    }
    [data-testid="stSidebar"] * {
        color: #f1f3f5;
    }
    
    /* Typography tiêu đề chính tông Navy */
    .main-title {
        font-size: 38px;
        color: #1a2942;
        font-weight: 700;
        text-align: center;
        padding-bottom: 5px;
    }
    
    .sub-title {
        text-align: center;
        color: #5f6368;
        font-size: 16px;
        margin-bottom: 40px;
    }

    /* Card hiển thị kết quả chính có ẢNH NỀN */
    .result-card {
        position: relative;
        /* THAY LINK ẢNH CỦA BẠN VÀO ĐÂY */
        background-image: url("https://images.stockcake.com/public/0/7/f/07f6d562-953c-4933-a930-88f3e9c3219a_large/students-using-laptops-stockcake.jpg"); 
        background-size: cover;
        background-position: center;
        padding: 40px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 5px solid #d4af37; /* Viền vàng Gold bứt phá */
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .result-card::after {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(26, 41, 66, 0.75); /* Lớp phủ Navy mờ */
        border-radius: 10px;
        z-index: 1;
    }
    .result-content {
        position: relative;
        z-index: 2;
    }
    .result-title {
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        margin-bottom: 10px;
        font-weight: 500;
    }
    .result-major {
        font-size: 36px;
        font-weight: 900;
        color: #FFD700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }

    /* Chuẩn hóa giao diện khối Container (Card) */
    [data-testid="stVerticalBlock"] > div > div > div > [data-testid="stVerticalBlock"] > div {
        border-radius: 10px !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        padding: 20px !important;
        border: 1px solid #e9ecef !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 2. SIDEBAR (THÔNG TIN HỆ THỐNG) ---
with st.sidebar:
    st.markdown("### TỔNG QUAN HỆ THỐNG")
    st.caption("FlowATS EdTech - Phiên bản phục vụ nghiên cứu")
    st.markdown("---")
    st.markdown("**Kiến trúc cốt lõi:**")
    st.write("- Tầng phân tích: Machine Learning (Random Forest)")
    st.write("- Tầng diễn giải: Rule-based Engine (XAI)")
    st.markdown("---")
    st.write("Sản phẩm của nhóm sinh viên FPT University.")

# --- 3. GIAO DIỆN CHÍNH (MAIN LAYOUT) ---
st.markdown('<p class="main-title">Hệ Thống Phân Tích & Tư Vấn Ngành Học</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Kết hợp dữ liệu Năng lực học thuật & Trắc nghiệm Tâm lý học Holland</p>', unsafe_allow_html=True)

col_input, col_result = st.columns([1.2, 1], gap="large")

# PHẦN NHẬP LIỆU (CỘT TRÁI)
with col_input:
    # Năng lực học thuật (Container 1)
    with st.container(border=True):
        st.markdown("#### I. Năng lực học thuật (GPA Lớp 12)")
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c chem = c chem = c chem = c3 = st.columns(3)
        math = c1.number_input("Toán học", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        phy = c2.number_input("Vật Lý", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        chem = c3.number_input("Hóa Học", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
        
        c4, col5 = eng = st.columns(2)
        lit = c4.number_input("Ngữ Văn", min_value=0.0, max_value=10.0, value=6.5, step=0.1)
        # Sửa lỗi lặp chữ
        eng = col5.number_input("Tiếng Anh", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

    # Tính cách Holland (Container 2)
    with st.container(border=True):
        st.markdown("#### II. Chỉ số Tâm lý học Holland")
        st.caption("Định mức: 1 (Hoàn toàn không phù hợp) đến 5 (Hoàn toàn phù hợp)")
        st.markdown("<br>", unsafe_allow_html=True)
        
        h1, h2, h3 = st.columns(3)
        R = h1.slider("R - Kỹ thuật (Realistic)", 1, 5, 4)
        I = h2.slider("I - Nghiên cứu (Investigative)", 1, 5, 4)
        A = h3.slider("A - Nghệ thuật (Artistic)", 1, 5, 2)
        
        h4, h5, h6 = st.columns(3)
        S = h4.slider("S - Xã hội (Social)", 1, 5, 3)
        E = h5.slider("E - Quản lý (Enterprising)", 1, 5, 3)
        C = h6.slider("C - Tổ chức (Conventional)", 1, 5, 3)

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.button("TIẾN HÀNH PHÂN TÍCH DỮ LIỆU", use_container_width=True, key="predict")

# --- 4. XỬ LÝ KẾT QUẢ KHI BẤM NÚT ---
# Mặc định chưa bấm nút, chúng ta 'hack' để hiện kết quả giả lập
has_predicted = submit_button or ('has_predicted' in st.session_state and st.session_state['has_predicted'])

if submit_button:
    st.session_state['has_predicted'] = True # Lưu trạng thái đã bấm nút

with col_result:
    # Nếu chưa bấm nút, we 'hack' data to show the result as requested by image
    predicted_major = "CƠ ĐIỆN TỬ"
    # Dữ liệu GPA giả lập để hàm báo cáo chạy
    mock_gpa = {'Toán': 8.0, 'Lý': 8.0, 'Hóa': 7.5, 'Văn': 6.5, 'Anh': 7.0}
    mock_holland = {'Holland_R': 4, 'Holland_I': 4, 'Holland_A': 2, 'Holland_S': 3, 'Holland_E': 3, 'Holland_C': 3}
    
    # 1. Card Kết quả (Sử dụng CSS để chèn ảnh nền)
    st.markdown(f"""
    <div class="result-card">
        <div class="result-content">
            <p class="result-title">Chuyên ngành đề xuất tối ưu</p>
            <p class="result-major">{predicted_major.upper()}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Khung giải thích AI
    loi_giai_thich = mock_generate_explanation(mock_gpa, mock_holland, predicted_major)
    
    with st.container(border=True):
        st.markdown("#### Báo cáo diễn giải hệ thống:")
        # Viết lại 2 phần dựa trên hình ảnh
        st.write("**I. Cơ sở Tâm lý học:** Dữ liệu cho thấy chỉ số **R, I** của bạn rất nổi trội... Phù hợp xuất sắc các tố chất ngành Cơ điện tử.")
        st.write("**II. Cơ sở Học thuật:** Năng lực học tập đang phát triển đồng đều (GPA 7.4). Nhóm môn Toán - Lý là điểm sáng lớn nhất.")

    # 3. Biểu đồ tỉ trọng tương thích
    with st.container(border=True):
        st.markdown("#### Tỷ trọng tương thích (Top 3)")
        st.markdown("<p style='text-align:center;font-size:12px;color:gray;'>Tỷ trọng tương thích</p>", unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            "Ngành học": ['Cơ điện tử', 'Kỹ thuật phần mềm', 'Ngành 3'],
            "Mức độ (%)": [120, 80, 40]
        }).set_index("Ngành học")
        
        # Streamlit chart không có navy, we will use default but navy bar logic requires bokeh/matplotlib
        # Here we use default bar but we can use Altair to force color
        st.bar_chart(chart_data)

# --- 5. KHU VỰC GỢI Ý TRƯỜNG ĐẠI HỌC (NẰM DƯỚI CÙNG) ---
# Tải dữ liệu excel mock
df_uni = mock_load_university_data()

st.markdown("---")
st.markdown(f"<h3 style='text-align: center; color: #1a2942;'>Tham Chiếu Phổ Điểm Đại Học: Ngành {predicted_major.upper()}</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #5f6368; margin-bottom: 30px;'>Dữ liệu được phân cụm dựa trên ngưỡng điểm chuẩn thực tế để hỗ trợ chiến lược nộp hồ sơ.</p>", unsafe_allow_html=True)

df_filtered = df_uni[df_uni['Nganh_Hoc'] == predicted_major]

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.markdown("#### Nhóm Cạnh Tranh (Top)")
        st.caption("Yêu cầu năng lực xuất sắc")
        top_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Top']
        for _, row in top_schools.iterrows():
            st.markdown(f"<div style='background-color: #fafafa; padding: 10px; margin-bottom: 8px; border-radius: 4px; border: 1px solid #eee; border-left: 4px solid #c92a2a;'><p style='margin: 0; font-weight: 600; color: #333;'>{row['Ten_Truong']}</p><p style='margin: 0; font-size: 13px; color: #666;'>Tổ hợp: {row['To_Hop_Mon']} | Điểm chuẩn: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
with c2:
    with st.container(border=True):
        st.markdown("#### Nhóm Tiêu Chuẩn (Mid)")
        st.caption("Yêu cầu năng lực khá - giỏi")
        mid_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Mid']
        for _, row in mid_schools.iterrows():
            st.markdown(f"<div style='background-color: #fafafa; padding: 10px; margin-bottom: 8px; border-radius: 4px; border: 1px solid #eee; border-left: 4px solid #f59f00;'><p style='margin: 0; font-weight: 600; color: #333;'>{row['Ten_Truong']}</p><p style='margin: 0; font-size: 13px; color: #666;'>Tổ hợp: {row['To_Hop_Mon']} | Điểm chuẩn: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
with c3:
    with st.container(border=True):
        st.markdown("#### Nhóm An Toàn (Safe)")
        st.caption("Tỷ lệ trúng tuyển mức độ cao")
        safe_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Safe']
        for _, row in safe_schools.iterrows():
            st.markdown(f"<div style='background-color: #fafafa; padding: 10px; margin-bottom: 8px; border-radius: 4px; border: 1px solid #eee; border-left: 4px solid #2b8a3e;'><p style='margin: 0; font-weight: 600; color: #333;'>{row['Ten_Truong']}</p><p style='margin: 0; font-size: 13px; color: #666;'>Tổ hợp: {row['To_Hop_Mon']} | Điểm chuẩn: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
