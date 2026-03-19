import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- 0. HÀM GIẢI THÍCH AI (Giữ nguyên logic cực xịn) ---
def generate_explanation(gpa_dict, holland_dict, major_name):
    holland_attributes = {
        'Holland_R': 'thích làm việc với công cụ, máy móc, thực hành và vận động',
        'Holland_I': 'tư duy logic, thích quan sát, phân tích và giải quyết vấn đề',
        'Holland_A': 'có tâm hồn phong phú, tư duy thẩm mỹ và thích sáng tạo',
        'Holland_S': 'thân thiện, thích kết nối, giúp đỡ và chăm sóc người khác',
        'Holland_E': 'có tố chất lãnh đạo, thích thuyết phục và kinh doanh',
        'Holland_C': 'làm việc ngăn nắp, cẩn thận, thích làm việc với số liệu'
    }

    gpa_attributes = {
        'Toán': 'tư duy logic',
        'Lý': 'khả năng phân tích kỹ thuật',
        'Hóa': 'tư duy thực nghiệm',
        'Văn': 'khả năng thấu cảm và ngôn ngữ',
        'Anh': 'tư duy hội nhập và ngoại ngữ'
    }

    # Xử lý Holland
    max_holland_score = max(holland_dict.values())
    top_hollands = [k for k, v in holland_dict.items() if v == max_holland_score]
    
    if len(top_hollands) == len(holland_dict):
        holland_cmt = f"Hiện tại, bài test cho thấy các nét tính cách của bạn đang ở mức bão hòa (chưa có nhóm nào thực sự vượt trội). Ngành **{major_name}** có thể là một môi trường mở để bạn vừa học vừa tiếp tục khám phá bản thân."
    else:
        top_h_names = ", ".join([h.replace('Holland_', '') for h in top_hollands])
        top_h_attrs = " và ".join([holland_attributes[h] for h in top_hollands])
        if max_holland_score <= 2:
            holland_cmt = f"Các nét tính cách của bạn chưa bộc lộ quá mạnh, nhưng nhóm **{top_h_names}** đang nhỉnh hơn đôi chút. Người mang đặc điểm này thường {top_h_attrs}. Ngành **{major_name}** khá phù hợp với định hướng này."
        else:
            holland_cmt = f"Hệ thống nhận thấy bạn có chỉ số **{top_h_names}** vô cùng nổi trội. Bạn là người {top_h_attrs}. Đặc điểm này cực kỳ ăn khớp với tính chất công việc của ngành **{major_name}**."

    # Xử lý GPA
    max_gpa = max(gpa_dict.values())
    top_subjects = [k for k, v in gpa_dict.items() if v == max_gpa]

    if len(top_subjects) == len(gpa_dict):
        if max_gpa < 5.0:
            gpa_cmt = f"Học lực hiện tại của bạn ở các môn đang bằng nhau ở mức ({max_gpa}). Để tự tin theo đuổi ngành **{major_name}**, bạn thực sự cần một kế hoạch bứt phá kiến thức ngay từ bây giờ."
        else:
            gpa_cmt = f"Năng lực học tập của bạn đang phát triển rất đồng đều ({max_gpa}). Đây là nền tảng cực kỳ tốt để bạn linh hoạt làm quen với nhiều khía cạnh của ngành **{major_name}**."
    else:
        top_s_names = ", ".join(top_subjects)
        top_s_attrs = " kết hợp cùng ".join([gpa_attributes[s] for s in top_subjects])
        if max_gpa < 5.0:
            gpa_cmt = f"Trong các môn, **{top_s_names} ({max_gpa})** đang là điểm khả quan nhất. Ngành **{major_name}** đòi hỏi {top_s_attrs}, do đó bạn sẽ cần nỗ lực cải thiện rất nhiều nền tảng này."
        elif max_gpa < 7.5:
            gpa_cmt = f"Nhóm môn **{top_s_names} ({max_gpa})** đang là thế mạnh của bạn, cho thấy tiềm năng về {top_s_attrs}. Đây là cơ sở khá ổn để bắt đầu với **{major_name}**."
        else:
            gpa_cmt = f"Điểm số môn **{top_s_names} ({max_gpa})** đang là một điểm sáng lớn. Điều này minh chứng cho {top_s_attrs} sắc bén, tạo bệ phóng vô cùng vững chắc để bứt phá trong ngành **{major_name}**."

    explanation = f"**Về tính cách:** {holland_cmt}\n\n**Về học thuật:** {gpa_cmt}"
    return explanation

# --- 1. CẤU HÌNH GIAO DIỆN & CSS CUSTOM ---
st.set_page_config(page_title="FlowATS EdTech - AI Hướng Nghiệp", page_icon="🧭", layout="wide")

custom_css = """
<style>
    /* Chỉnh màu nền tổng thể về tông màu "gỗ, giấy" nhạt */
    .stApp {
        background-color: #fcfaf6;
        color: #333333;
    }
    
    /* Chỉnh sidebar về tông màu xanh navy đậm chuyên nghiệp */
    [data-testid="stSidebar"] {
        background-color: #1e3c72;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white;
    }
    
    /* Tiêu đề chính tông navy đậm học thuật */
    .main-title {
        font-size: 42px;
        color: #1e3c72;
        font-weight: 800;
        text-align: center;
        padding-bottom: 10px;
        font-family: 'Playfair Display', serif; /* Font chữ mang đậm chất học đường */
    }
    
    .sub-title {
        text-align: center;
        color: #6c757d;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* Card Kết quả AI tông navy đậm đáng tin cậy */
    .result-card {
        background-color: #1e3c72;
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
        border: 2px solid #FFD700; /* Viền vàng sang trọng */
        animation: fadeIn 1s ease-in-out;
    }
    .result-title {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 8px;
    }
    .result-major {
        font-size: 36px;
        font-weight: 900;
        color: #FFD700;
        margin: 0;
    }

    /* Bo góc, shadow nhẹ cho các Container */
    [data-testid="stVerticalBlock"] > div > div > div > [data-testid="stVerticalBlock"] > div {
        border-radius: 10px !important;
        background-color: white !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        padding: 15px !important;
    }
    
    /* Hiệu ứng Fade In */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 2. TẢI "BỘ NÃO" AI VÀ DATABASE ---
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
    st.error(f"⚠️ Lỗi tải dữ liệu. Lỗi: {e}")
    st.stop()

# --- 3. SIDEBAR (THANH ĐIỀU HƯỚNG BÊN TRÁI) ---
with st.sidebar:
    # Icon La bàn định hướng mang tính học thuật
    st.image("https://cdn-icons-png.flaticon.com/512/323/323041.png", width=100)
    st.markdown("### 🗺 FlowATS: Hướng Nghiệp")
    st.caption("Phiên bản EdTech - Một Sản Phẩm của Sinh Viên FPT University.")
    st.markdown("---")
    st.markdown("### 📚 Công nghệ & Phương pháp:")
    st.write("📖 **Cốt lõi:** Machine Learning (Random Forest)")
    st.write("🎓 **Hỗ trợ:** Explainable AI (Rule-based Engine)")
    st.write("⚙️ **Kỹ thuật:** SMOTE (Data Balancing)")
    st.markdown("---")
    st.write("🌐 Nền tảng tư vấn End-to-End.")

# --- 4. GIAO DIỆN CHÍNH ---
st.markdown('<p class="main-title">🌐 Hệ Thống Tư Vấn Ngành Học & Chọn Trường</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Kết hợp Năng lực học thuật & Tâm lý học Holland để tìm ra bệ phóng tương lai của bạn</p>', unsafe_allow_html=True)

# Layout chia làm 2 cột: Cột trái (Nhập liệu) - Cột phải (Kết quả)
col_input, col_result = st.columns([1.2, 1], gap="large")

with col_input:
    with st.form("user_input_form"):
        # Box 1: Điểm số
        with st.container(border=True):
            # Icon sách và cây bút
            col_icon_1, col_text_1 = st.columns([0.15, 1])
            col_icon_1.image("https://cdn-icons-png.flaticon.com/512/29/29302.png", width=30)
            col_text_1.markdown("#### 📖 1. Năng lực học thuật (GPA Lớp 12)")
            
            c1, c2, c3 = st.columns(3)
            math = c1.number_input("Toán", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
            phy = c2.number_input("Vật Lý", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
            chem = c3.number_input("Hóa Học", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
            
            c4, c5 = st.columns(2)
            lit = c4.number_input("Ngữ Văn", min_value=0.0, max_value=10.0, value=6.5, step=0.1)
            eng = col5 = eng = st.number_input("Tiếng Anh", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

        # Box 2: Tính cách
        with st.container(border=True):
            # Icon kính lúp và mảnh ghép
            col_icon_2, col_text_2 = st.columns([0.15, 1])
            col_icon_2.image("https://cdn-icons-png.flaticon.com/512/1000/1000302.png", width=30)
            col_text_2.markdown("#### 🧠 2. Đặc điểm tính cách Holland")
            st.caption("Kéo thanh trượt từ 1 (Không giống tôi) đến 5 (Rất giống tôi)")
            
            h1, h2, h3 = st.columns(3)
            R = h1.slider("R - Kỹ thuật", 1, 5, 4)
            I = h2.slider("I - Nghiên cứu", 1, 5, 4)
            A = h3.slider("A - Nghệ thuật", 1, 5, 2)
            
            h4, h5, h6 = st.columns(3)
            S = h4.slider("S - Xã hội", 1, 5, 3)
            E = h5.slider("E - Quản lý", 1, 5, 3)
            C = h6.slider("C - Tổ chức", 1, 5, 3)

        # Nút bấm submit bự
        st.markdown("<br>", unsafe_allow_html=True)
        # Thay robot bằng tên lửa cho nút bấm
        submit_button = st.form_submit_button("🎓 BẮT ĐẦU PHÂN TÍCH HỒ SƠ", use_container_width=True)

# --- 5. XỬ LÝ KẾT QUẢ ---
with col_result:
    if submit_button:
        with st.spinner("AI đang tổng hợp và phân tích dữ liệu..."):
            # Dự đoán
            user_input = np.array([[math, phy, chem, lit, eng, R, I, A, S, E, C]])
            user_scaled = scaler.transform(user_input)
            
            all_probs = rf_model.predict_proba(user_scaled)[0]
            top_3_indices = np.argsort(all_probs)[-3:][::-1]
            top_3_majors = label_encoder.inverse_transform(top_3_indices)
            top_3_probs_raw = all_probs[top_3_indices]
            
            boosted_probs = top_3_probs_raw ** 2  
            top_3_probs_scaled = (boosted_probs / np.sum(boosted_probs)) * 100
            predicted_major = top_3_majors[0]
            
            # Khung HTML hiển thị kết quả siêu xịn, tông navy vàng gold
            st.markdown(f"""
            <div class="result-card">
                <p class="result-title">🎓 NGÀNH HỌC PHÙ HỢP NHẤT VỚI BẠN</p>
                <p class="result-major">{predicted_major.upper()}</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
            
            # Hộp thông tin giải thích AI
            user_gpa = {'Toán': math, 'Lý': phy, 'Hóa': chem, 'Văn': lit, 'Anh': eng}
            user_holland = {'Holland_R': R, 'Holland_I': I, 'Holland_A': A, 'Holland_S': S, 'Holland_E': E, 'Holland_C': C}
            
            loi_giai_thich = generate_explanation(user_gpa, user_holland, predicted_major)
            
            with st.container(border=True):
                # Icon mũ cử nhân
                st.image("https://cdn-icons-png.flaticon.com/512/93/93634.png", width=30)
                st.markdown("### 🎓 Lời gợi ý của hệ thống:")
                st.write(loi_giai_thich)
            
            # Biểu đồ Top 3
            with st.container(border=True):
                # Icon biểu đồ cột phẳng, tông màu xanh xám học thuật
                st.markdown("### 📊 Mức độ tương thích")
                chart_data = pd.DataFrame({"Ngành học": top_3_majors, "Mức độ (%)": top_3_probs_scaled}).set_index("Ngành học")
                st.bar_chart(chart_data)

# --- 6. KHU VỰC GỢI Ý TRƯỜNG ĐẠI HỌC (NẰM DƯỚI CÙNG, TRẢI DÀI) ---
if submit_button and df_uni is not None:
    st.markdown("---")
    # Icon trường đại học
    st.image("https://cdn-icons-png.flaticon.com/512/1000/1000301.png", width=40)
    st.markdown(f"<h3 style='text-align: center;'>🏫 DANH SÁCH TRƯỜNG ĐÀO TẠO NGÀNH {predicted_major.upper()}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Hệ thống phân loại các trường dựa trên điểm chuẩn thực tế để bạn xây dựng chiến lược nộp hồ sơ.</p>", unsafe_allow_html=True)
    
    df_filtered = df_uni[df_uni['Nganh_Hoc'] == predicted_major]
    
    if not df_filtered.empty:
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True):
                st.markdown("#### 🔥 Nhóm Ước Mơ (Top)")
                st.caption("Điểm chuẩn rất cao, tính cạnh tranh khốc liệt")
                top_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Top']
                for _, row in top_schools.iterrows():
                    # Thay đổi tông màu sang đỏ đậm, không còn gradient lấp lánh
                    st.markdown(f"<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 5px solid #dc3545;'><p style='margin: 0;'><strong>{row['Ten_Truong']}</strong></p><p style='margin: 0;'>Khối: {row['To_Hop_Mon']} | Điểm: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
        with c2:
            with st.container(border=True):
                st.markdown("#### ⭐ Nhóm Vừa Sức (Mid)")
                st.caption("Điểm chuẩn mức khá, phù hợp với năng lực")
                mid_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Mid']
                for _, row in mid_schools.iterrows():
                    # Tông màu vàng đậm học thuật
                    st.markdown(f"<div style='background-color: #fff3cd; padding: 10px; border-radius: 5px; border-left: 5px solid #ffc107;'><p style='margin: 0;'><strong>{row['Ten_Truong']}</strong></p><p style='margin: 0;'>Khối: {row['To_Hop_Mon']} | Điểm: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
        with c3:
            with st.container(border=True):
                st.markdown("#### ✅ Nhóm An Toàn (Safe)")
                st.caption("Điểm chuẩn vừa phải, tỷ lệ đỗ cao")
                safe_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Safe']
                for _, row in safe_schools.iterrows():
                    # Tông màu xanh lá đậm học thuật
                    st.markdown(f"<div style='background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid #28a745;'><p style='margin: 0;'><strong>{row['Ten_Truong']}</strong></p><p style='margin: 0;'>Khối: {row['To_Hop_Mon']} | Điểm: <strong>{row['Diem_Chuan']}</strong></p></div>", unsafe_allow_html=True)
    else:
        st.warning(f"Hệ thống đang cập nhật dữ liệu điểm chuẩn cho ngành {predicted_major}.")
