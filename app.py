import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

def generate_explanation(gpa_dict, holland_dict, major_name):
    """
    Hàm tự động sinh lời giải thích với logic kiểm tra ngưỡng điểm và xử lý ĐỒNG HẠNG.
    """
    # 1. Từ điển thuộc tính
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

    # 2. Xử lý ĐỒNG HẠNG cho Holland
    max_holland_score = max(holland_dict.values())
    top_hollands = [k for k, v in holland_dict.items() if v == max_holland_score]
    
    # Nếu tất cả các nhóm tính cách đều bằng nhau (kéo full 1 hoặc full 5)
    if len(top_hollands) == len(holland_dict):
        holland_cmt = f"Hiện tại, bài test cho thấy các nét tính cách của bạn đang ở mức bão hòa (chưa có nhóm nào thực sự vượt trội). Trong thời gian tới, hãy trải nghiệm nhiều hơn để tìm ra thế mạnh cốt lõi của mình nhé. Ngành {major_name} có thể là một môi trường mở để bạn khám phá bản thân."
    else:
        # Nếu có 1 hoặc vài nhóm cao nhất
        top_h_names = ", ".join([h.replace('Holland_', '') for h in top_hollands])
        top_h_attrs = " và ".join([holland_attributes[h] for h in top_hollands])
        
        if max_holland_score <= 2:
            holland_cmt = f"Các nét tính cách của bạn chưa bộc lộ quá mạnh, nhưng nhóm **{top_h_names}** đang nhỉnh hơn đôi chút. Người mang đặc điểm này thường {top_h_attrs}. Ngành {major_name} khá phù hợp với định hướng này."
        else:
            holland_cmt = f"Hệ thống nhận thấy bạn có chỉ số **{top_h_names}** vô cùng nổi trội. Bạn là người {top_h_attrs}. Đặc điểm này cực kỳ ăn khớp với tính chất công việc của ngành {major_name}."

    # 3. Xử lý ĐỒNG HẠNG cho GPA
    max_gpa = max(gpa_dict.values())
    top_subjects = [k for k, v in gpa_dict.items() if v == max_gpa]

    # Nếu tất cả các môn đều bằng điểm nhau (ví dụ: full 3.0 hoặc full 9.0)
    if len(top_subjects) == len(gpa_dict):
        if max_gpa < 5.0:
            gpa_cmt = f"Học lực hiện tại của bạn ở các môn đang bằng nhau ở mức **({max_gpa})**. Để có thể tự tin theo đuổi ngành {major_name}, bạn thực sự cần một kế hoạch bứt phá và cải thiện nền tảng kiến thức ngay từ bây giờ."
        else:
            gpa_cmt = f"Năng lực học tập của bạn đang phát triển rất đồng đều ở tất cả các môn với mức điểm **({max_gpa})**. Đây là một nền tảng tổng hợp cực kỳ tốt để bạn có thể linh hoạt làm quen với nhiều khía cạnh của ngành {major_name}."
    else:
        # Nếu có 1 hoặc vài môn cao nhất
        top_s_names = ", ".join(top_subjects)
        top_s_attrs = " kết hợp cùng ".join([gpa_attributes[s] for s in top_subjects])
        
        if max_gpa < 5.0:
            gpa_cmt = f"Trong các môn học, **{top_s_names} ({max_gpa})** đang là điểm sáng nhất của bạn. Ngành {major_name} đòi hỏi {top_s_attrs}, do đó bạn sẽ cần nỗ lực cải thiện rất nhiều nền tảng này."
        elif max_gpa < 7.5:
            gpa_cmt = f"Nhóm môn **{top_s_names} ({max_gpa})** đang là thế mạnh của bạn. Nó cho thấy tiềm năng về {top_s_attrs}, là cơ sở khá ổn để bắt đầu với {major_name}."
        else:
            gpa_cmt = f"Điểm số môn **{top_s_names} ({max_gpa})** đang là một điểm sáng lớn trong hồ sơ của bạn. Điều này minh chứng cho {top_s_attrs} sắc bén, tạo bệ phóng vô cùng vững chắc để bứt phá trong ngành {major_name}."

    # 4. Lắp ghép thành lời giải thích hoàn chỉnh
    explanation = f"""
**💡 Tại sao {major_name} lại được gợi ý cho bạn?**

* **Về đặc điểm tính cách:** {holland_cmt}
* **Về năng lực học thuật:** {gpa_cmt}
"""
    return explanation

# --- 1. CẤU HÌNH GIAO DIỆN WEB ---
st.set_page_config(page_title="AI Tư Vấn Chọn Ngành", page_icon="🎓", layout="centered")
st.title("🎓 Hệ Thống AI Tư Vấn Chọn Ngành Học")
st.markdown("---")
st.write("Nhập điểm phẩy cấp 3 và kết quả bài test tính cách Holland của bạn để hệ thống phân tích và đưa ra gợi ý ngành học phù hợp nhất!")

# --- 2. TẢI "BỘ NÃO" AI VÀ DATABASE TRƯỜNG ĐẠI HỌC ---
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

# --- 3. KHU VỰC NHẬP LIỆU CỦA NGƯỜI DÙNG ---
with st.form("user_input_form"):
    st.subheader("📚 1. Năng lực học thuật (GPA Lớp 12)")
    col1, col2, col3 = st.columns(3)
    math = col1.number_input("Toán", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
    phy = col2.number_input("Vật Lý", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
    chem = col3.number_input("Hóa Học", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
    
    col4, col5 = st.columns(2)
    lit = col4.number_input("Ngữ Văn", min_value=0.0, max_value=10.0, value=6.5, step=0.1)
    eng = col5.number_input("Tiếng Anh", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

    st.subheader("🧩 2. Tính cách Holland (Thang 1-5)")
    st.caption("(1: Hoàn toàn không giống | 5: Cực kỳ giống tôi)")
    
    h1, h2, h3 = st.columns(3)
    R = h1.slider("R - Kỹ thuật (Thực tế)", 1, 5, 4)
    I = h2.slider("I - Nghiên cứu", 1, 5, 4)
    A = h3.slider("A - Nghệ thuật", 1, 5, 2)
    
    h4, h5, h6 = st.columns(3)
    S = h4.slider("S - Xã hội", 1, 5, 3)
    E = h5.slider("E - Quản lý", 1, 5, 3)
    C = h6.slider("C - Nghiệp vụ", 1, 5, 3)

    submit_button = st.form_submit_button("🚀 Bắt Đầu Phân Tích!")

# --- 4. XỬ LÝ KHI BẤM NÚT ---
if submit_button:
    with st.spinner("Hệ thống đang tổng hợp dữ liệu và phân tích..."):
        # 1. Dự đoán Ngành học
        user_input = np.array([[math, phy, chem, lit, eng, R, I, A, S, E, C]])
        user_scaled = scaler.transform(user_input)
        
        # Lấy toàn bộ xác suất của 29 ngành
        all_probs = rf_model.predict_proba(user_scaled)[0]
        
        # Tìm ra vị trí của Top 3 ngành điểm cao nhất
        top_3_indices = np.argsort(all_probs)[-3:][::-1]
        top_3_majors = label_encoder.inverse_transform(top_3_indices)
        top_3_probs_raw = all_probs[top_3_indices]
        
        # Tính toán mức độ tương thích để vẽ biểu đồ
        boosted_probs = top_3_probs_raw ** 2  
        top_3_probs_scaled = (boosted_probs / np.sum(boosted_probs)) * 100
        
        # Ngành chiến thắng cuối cùng
        predicted_major = top_3_majors[0]
        
        # 2. Hiển thị Ngành học đề xuất (Không nhắc tới độ tự tin)
        st.success("✨ Phân tích hoàn tất!")
        st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>Ngành học đề xuất: {predicted_major}</h2>", unsafe_allow_html=True)
        st.balloons()
        
        # 3. GỌI HÀM VÀ IN LỜI GIẢI THÍCH
        user_gpa = {
            'Toán': math,
            'Lý': phy,
            'Hóa': chem,
            'Văn': lit,
            'Anh': eng
        }
        
        user_holland = {
            'Holland_R': R,
            'Holland_I': I,
            'Holland_A': A,
            'Holland_S': S,
            'Holland_E': E,
            'Holland_C': C
        }
        
        loi_giai_thich = generate_explanation(user_gpa, user_holland, predicted_major)
        st.info(loi_giai_thich)
        
        # 4. VẼ BIỂU ĐỒ TOP 3 NGÀNH (Sử dụng từ "Mức độ tương thích")
        st.markdown("### 📊 Top 3 Ngành Phù Hợp Nhất")
        
        chart_data = pd.DataFrame({
            "Ngành học": top_3_majors,
            "Mức độ tương thích (%)": top_3_probs_scaled
        }).set_index("Ngành học")
        
        st.bar_chart(chart_data)
        
        # 5. Lọc và hiển thị Trường Đại Học
        if df_uni is not None:
            st.markdown("---")
            st.subheader(f"🏫 Gợi ý trường Đại học đào tạo ngành {predicted_major}")
            st.write(f"*Dựa trên điểm chuẩn thực tế, hệ thống phân loại các trường để bạn tham khảo:*")
            
            df_filtered = df_uni[df_uni['Nganh_Hoc'] == predicted_major]
            
            if not df_filtered.empty:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.error("🔥 Nhóm Mơ ước (Top)\n*(Điểm chuẩn rất cao)*")
                    top_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Top']
                    for _, row in top_schools.iterrows():
                        st.markdown(f"**{row['Ten_Truong']}**\n- Khối: {row['To_Hop_Mon']}\n- Điểm: **{row['Diem_Chuan']}**")
                with c2:
                    st.warning("⭐ Nhóm Vừa sức (Mid)\n*(Điểm chuẩn mức khá)*")
                    mid_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Mid']
                    for _, row in mid_schools.iterrows():
                        st.markdown(f"**{row['Ten_Truong']}**\n- Khối: {row['To_Hop_Mon']}\n- Điểm: **{row['Diem_Chuan']}**")
                with c3:
                    st.success("✅ Nhóm An toàn (Safe)\n*(Điểm chuẩn vừa phải)*")
                    safe_schools = df_filtered[df_filtered['Phan_Loai_Truong'] == 'Safe']
                    for _, row in safe_schools.iterrows():
                        st.markdown(f"**{row['Ten_Truong']}**\n- Khối: {row['To_Hop_Mon']}\n- Điểm: **{row['Diem_Chuan']}**")
            else:
                st.warning(f"Hệ thống đang cập nhật dữ liệu điểm chuẩn cho ngành {predicted_major}.")
        else:
            st.error("Chưa tìm thấy file phan_loai_truong.xlsx! Hãy kiểm tra lại thư mục.")