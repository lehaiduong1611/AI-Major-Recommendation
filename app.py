import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- 1. HÀM GIẢI THÍCH AI (Logic hệ luật chuyên sâu) ---
def generate_explanation(gpa_dict, holland_dict, major_name):
    holland_attributes = {
        'Holland_R': 'thích làm việc với công cụ, thiết bị, ưu tiên thực hành và vận động',
        'Holland_I': 'tư duy logic, thích quan sát, phân tích và giải quyết vấn đề phức tạp',
        'Holland_A': 'có thế giới quan phong phú, tư duy thẩm mỹ và tính sáng tạo cao',
        'Holland_S': 'thiên hướng thân thiện, thích kết nối, hỗ trợ và phát triển con người',
        'Holland_E': 'có tố chất lãnh đạo, thích thuyết phục, đàm phán và quản lý',
        'Holland_C': 'làm việc có hệ thống, cẩn thận, ưu tiên tính chính xác và số liệu'
    }

    gpa_attributes = {
        'Toán': 'tư duy logic và định lượng',
        'Lý': 'khả năng phân tích hệ thống và kỹ thuật',
        'Hóa': 'tư duy khoa học và thực nghiệm',
        'Văn': 'năng lực tổng hợp ngôn ngữ và thấu cảm',
        'Anh': 'tư duy hội nhập và khả năng giao tiếp toàn cầu'
    }

    # Phân tích Holland
    max_holland_score = max(holland_dict.values())
    top_hollands = [k for k, v in holland_dict.items() if v == max_holland_score]
    
    if len(top_hollands) == len(holland_dict):
        holland_cmt = f"Kết quả đánh giá cho thấy các nhóm tính cách của bạn đang ở mức cân bằng. Ngành **{major_name}** là một môi trường mang tính đa chiều, phù hợp để bạn tiếp tục trải nghiệm và xác định rõ hơn thế mạnh cốt lõi của mình."
    else:
        top_h_names = ", ".join([h.replace('Holland_', '') for h in top_hollands])
        top_h_attrs = " và ".join([holland_attributes[h] for h in top_hollands])
        if max_holland_score <= 2:
            holland_cmt = f"Các đặc điểm tính cách chưa bộc lộ quá mạnh, tuy nhiên nhóm **{top_h_names}** đang có xu hướng nhỉnh hơn. Những cá nhân thuộc nhóm này thường {top_h_attrs}. Ngành **{major_name}** có môi trường khá tương đồng với định hướng này."
        else:
            holland_cmt = f"Dữ liệu cho thấy chỉ số **{top_h_names}** của bạn rất nổi trội. Bạn có xu hướng {top_h_attrs}. Đặc điểm này đáp ứng xuất sắc các yêu cầu về tố chất nghề nghiệp của ngành **{major_name}**."

    # Phân tích GPA
    max_gpa = max(gpa_dict.values())
    top_subjects = [k for k, v in gpa_dict.items() if v == max_gpa]

    if len(top_subjects) == len(gpa_dict):
        if max_gpa < 5.0:
            gpa_cmt = f"Phổ điểm hiện tại của bạn đang đồng đều ở mức ({max_gpa}). Để xây dựng lộ trình học tập hiệu quả cho ngành **{major_name}**, bạn cần có kế hoạch bổ sung kiến thức nền tảng ngay trong giai đoạn này."
        else:
            gpa_cmt = f"Năng lực tiếp thu của bạn đang duy trì sự đồng đều rất tốt ({max_gpa}). Đây là cơ sở dữ liệu tích cực chứng minh bạn có khả năng thích nghi linh hoạt với khối lượng kiến thức đa ngành của **{major_name}**."
    else:
        top_s_names = ", ".join(top_subjects)
        top_s_attrs = " kết hợp cùng ".join([gpa_attributes[s] for s in top_subjects])
        if max_gpa < 5.0:
            gpa_cmt = f"Trong hệ thống môn học, **{top_s_names} ({max_gpa})** đang là chỉ số khả quan nhất. Do ngành **{major_name}** yêu cầu cao về {top_s_attrs}, bạn cần thiết lập mục tiêu cải thiện rõ rệt các năng lực này."
        elif max_gpa < 7.5:
            gpa_cmt = f"Nhóm môn **{top_s_names} ({max_gpa})** đang bộc lộ là thế mạnh của bạn, phản ánh tiềm năng về {top_s_attrs}. Dữ liệu này cho thấy bạn có đủ điều kiện cơ sở để tiếp cận chuyên ngành **{major_name}**."
        else:
            gpa_cmt = f"Mức điểm **{top_s_names} ({max_gpa})** là một chỉ số ưu tú trong hồ sơ của bạn. Cấp độ này minh chứng cho {top_s_attrs} sắc bén, tạo lợi thế cạnh tranh rất lớn khi bạn theo học ngành **{major_name}**."

    explanation = f"**I. Cơ sở Tâm lý học:**\n{holland_cmt}\n\n**II. Cơ sở Học thuật:**\n{gpa_cmt}"
    return explanation

# --- 2. CẤU HÌNH GIAO DIỆN & CSS TÍCH HỢP ẢNH NỀN ---
st.set_page_config(page_title="AI Hướng Nghiệp - FPT University", layout="wide")

custom_css = """
<style>
    /* Nền tổng thể: Tối giản, sạch sẽ */
    .stApp {
        background-color: #fdfdfc;
        color: #2b2b2b;
    }
    
    /* Thiết kế Sidebar chuyên nghiệp, tông Navy đậm */
    [data-testid="stSidebar"] {
        background-color: #1a2942;
        color: #f1f3f5;
    }
    [data-testid="stSidebar"] * {
        color: #f1f3f5;
    }
    
    /* Typography tiêu đề chính tông Navy đậm */
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

    /* Card hiển thị kết quả tích hợp ẢNH NỀN CỦA BẠN */
    .result-card {
        position: relative;
        background-image: url("https://images.stockcake.com/public/0/7/f/07f6d562-953c-4933-a930-88f3e9c3219a_large/students-using-laptops-stockcake.jpg"); 
        background-size: cover;
        background-position: center;
        padding: 40px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 5px solid #d4af37; /* Điểm nhấn viền vàng Gold */
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Lớp phủ mờ (overlay) để chữ nổi bật hơn */
    .result-card::after {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(26, 41, 66, 0.75); /* Màu Navy đậm với độ mờ 75% */
        border-radius: 12px;
        z-index: 1;
    }
    
    /* Đưa chữ lên trên lớp phủ mờ */
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
        color: #FFD700; /* Màu vàng Gold rực rỡ */
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }

    /* Bo góc và bóng đổ nhẹ cho các Container */
    [data-testid="stVerticalBlock"] > div > div > div > [data-testid="stVerticalBlock"] > div {
        border-radius: 10px !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        padding: 20px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. KHỞI TẠO DỮ LIỆU ---
@st.cache_resource 
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model = joblib.load(os.path.join(base_dir, 'saved_models', 'best_model.pkl'))
    scaler = joblib.load(os.path.join(base_dir, 'saved_models', 'scaler.pkl'))
    label_encoder = joblib.load(os.path.join(base_dir, 'saved_models', 'label_encoder.pkl'))
    return model, scaler, label_encoder

@st.cache_data
def load_university_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, 'phan_loai_truong.xlsx') 
    if os.path.exists(excel_path):
        return pd.read_excel(excel_path) 
    return None

try:
    rf_model, scaler, label_encoder = load_models()
    df_uni = load_university_data()
except Exception as e:
    st.error(f"Sự cố hệ thống khi tải dữ liệu. Chi tiết mã lỗi: {e}")
    st.stop()

# --- 4. SIDEBAR (THÔNG TIN HỆ THỐNG) ---
with st.sidebar:
    st.markdown("### TỔNG QUAN HỆ THỐNG")
    st.caption("FlowATS EdTech - Phiên bản phục vụ nghiên cứu")
    st.markdown("---")
    st.markdown("**Kiến trúc cốt lõi:**")
    st.write("- Tầng phân tích: Random Forest (AI)")
    st.write("- Tầng diễn giải: Rule-based Engine (XAI)")
    st.markdown("---")
    st.write("Sản phẩm của nhóm sinh viên FPT University.")

# --- 5. GIAO DIỆN CHÍNH (MAIN LAYOUT) ---
st.markdown('<p class="main-title">Hệ Thống Phân Tích & Tư Vấn Ngành Học</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Kết hợp dữ liệu Năng lực học thuật & Trắc nghiệm Tâm lý học Holland</p>', unsafe_allow_html=True)

col_input, col_result = st.columns([1.2, 1], gap="large")

# PHẦN NHẬP LIỆU (CỘT TRÁI - NỀN TRẮNG SẠCH SẼ)
with col_input:
    with st.form("user_input_form"):
        with st.container(border=True):
            st.markdown("#### I. Năng lực học thuật (GPA Lớp 12)")
            st.markdown("<br>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            math = c1.number_input("Toán học", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
            phy = c2.number_input("Vật Lý", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
            chem = c3.number_input("Hóa Học", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
            
            c4, c5 = st.columns(2)
            lit = c4.number_input("Ngữ Văn", min_value=0.0, max_value=10.0, value=6.5, step=0.1)
            eng = c5.number_input("Tiếng Anh", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

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
        submit_button = st.form_submit_button("TIẾN HÀNH PHÂN TÍCH DỮ LIỆU", use_container_width=True)

# PHẦN KẾT QUẢ (CỘT PHẢI - TÍCH HỢP ẢNH NỀN)
with col_result:
    if submit_button:
        with st.spinner("Hệ thống đang xử lý thuật toán..."):
            # Chạy model
            user_input = np.array([[math, phy, chem, lit, eng, R, I, A, S, E, C]])
            user_scaled = scaler.transform(user_input)
            
            all_probs = rf_model.predict_proba(user_scaled)[0]
            top_3_indices = np.argsort(all_probs)[-3:][::-1]
            top_3_majors = label_encoder.inverse_transform(top_3_indices)
            top_3_probs_raw = all_probs[top_3_indices]
            
            boosted_probs = top_3_probs_raw ** 2  
            top_3_probs_scaled = (boosted_probs / np.sum(boosted_probs)) * 100
            predicted_major = top_3_majors[0]
            
            # Khung HTML hiển thị kết quả TÍCH HỢP ẢNH NỀN
            st.markdown(f"""
            <div class="result-card">
                <div class="result-content">
                    <p class="result-title">Chuyên ngành đề xuất tối ưu</p>
                    <p class="result-major">{predicted_major.upper()}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hộp thông tin giải thích AI
            user_gpa = {'Toán': math, 'Lý': phy, 'Hóa': chem, 'Văn': lit, 'Anh': eng}
            user_holland = {'Holland_R': R, 'Holland_I': I, 'Holland_A': A, 'Holland_S': S, 'Holland_E': E, 'Holland_C': C}
            
            loi_giai_thich = generate_explanation(user_gpa, user_holland, predicted_major)
            
            with st.container(border=True):
                st.markdown("#### Báo cáo diễn giải hệ thống:")
                st.write(loi_giai_thich)
            
            # Biểu đồ Top 3
            with st.container(border=True):
                st.markdown("#### Tỷ trọng tương thích (Top 3)")
                chart_data = pd.DataFrame({"Ngành học": top_3_majors, "Mức độ (%)": top_3_probs_scaled}).set_index("Ngành học")
                st.bar_chart(chart_data)

# --- 6. PHÂN TÍCH TRƯỜNG ĐẠI HỌC (DÀN TRẢI DƯỚI CÙNG) ---
if submit_button and df_uni is not None:
    st.markdown("---")
    st.markdown(f"<h3 style='text-align: center; color: #1a2942;'>Tham Chiếu Phổ Điểm Đại Học: Ngành {predicted_major.upper()}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #5f6368; margin-bottom: 30px;'>Dữ liệu được phân cụm dựa trên ngưỡng điểm chuẩn thực tế để hỗ trợ chiến lược nộp hồ sơ.</p>", unsafe_allow_html=True)
    
    df_filtered = df_uni[df_uni['Nganh_Hoc'] == predicted_major]
    
    if not df_filtered.empty:
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.markdown("#### Nhóm Cạnh Tranh (Top)")
                st.caption("Yêu cầu năng lực xuất sắc")
                top_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Top']
                for _, row in top_schools.iterrows():
                    st.markdown(f"<div style='background-color: #fafafa; padding: 12px; margin-bottom: 8px; border-radius: 4px; border: 1px solid #eee; border-left: 4px solid #c92a2a;'><p style='margin: 0; font-weight: 600; color: #333;'>{row['Ten_Truong']}</p><p style='margin: 0; font-size: 13px; color: #666;'>Tổ hợp: {row['To_Hop_Mon']} | Điểm chuẩn: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
        with c2:
            with st.container(border=True):
                st.markdown("#### Nhóm Tiêu Chuẩn (Mid)")
                st.caption("Yêu cầu năng lực khá - giỏi")
                mid_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Mid']
                for _, row in mid_schools.iterrows():
                    st.markdown(f"<div style='background-color: #fafafa; padding: 12px; margin-bottom: 8px; border-radius: 4px; border: 1px solid #eee; border-left: 4px solid #f59f00;'><p style='margin: 0; font-weight: 600; color: #333;'>{row['Ten_Truong']}</p><p style='margin: 0; font-size: 13px; color: #666;'>Tổ hợp: {row['To_Hop_Mon']} | Điểm chuẩn: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
        with c3:
            with st.container(border=True):
                st.markdown("#### Nhóm An Toàn (Safe)")
                st.caption("Tỷ lệ trúng tuyển mức độ cao")
                safe_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Safe']
                for _, row in safe_schools.iterrows():
                    st.markdown(f"<div style='background-color: #fafafa; padding: 12px; margin-bottom: 8px; border-radius: 4px; border: 1px solid #eee; border-left: 4px solid #2b8a3e;'><p style='margin: 0; font-weight: 600; color: #333;'>{row['Ten_Truong']}</p><p style='margin: 0; font-size: 13px; color: #666;'>Tổ hợp: {row['To_Hop_Mon']} | Điểm chuẩn: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
    else:
        st.info(f"Hệ thống đang trong quá trình đồng bộ hóa phổ điểm cho chuyên ngành {predicted_major}.")
