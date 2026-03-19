import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- 1. HÀM GIẢI THÍCH AI ---
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

    max_gpa = max(gpa_dict.values())
    top_subjects = [k for k, v in gpa_dict.items() if v == max_gpa]

    if len(top_subjects) == len(gpa_dict):
        if max_gpa < 5.0:
            gpa_cmt = f"Phổ điểm hiện tại của bạn đang đồng đều ở mức ({max_gpa}). Để xây dựng lộ trình học tập hiệu quả cho ngành **{major_name}**, bạn cần có kế hoạch bổ sung kiến thức nền tảng ngay trong giai đoạn này."
        else:
            gpa_cmt = f"Năng lực tiếp thu của bạn đang duy trì sự đồng đều rất tốt ({max_gpa}). Đây là cơ sở tích cực chứng minh bạn có khả năng thích nghi linh hoạt với khối lượng kiến thức đa ngành của **{major_name}**."
    else:
        top_s_names = ", ".join(top_subjects)
        top_s_attrs = " kết hợp cùng ".join([gpa_attributes[s] for s in top_subjects])
        if max_gpa < 5.0:
            gpa_cmt = f"Trong hệ thống môn học, **{top_s_names} ({max_gpa})** đang là chỉ số khả quan nhất. Do ngành **{major_name}** yêu cầu cao về {top_s_attrs}, bạn cần thiết lập mục tiêu cải thiện rõ rệt các năng lực này."
        elif max_gpa < 7.5:
            gpa_cmt = f"Nhóm môn **{top_s_names} ({max_gpa})** đang bộc lộ là thế mạnh của bạn, phản ánh tiềm năng về {top_s_attrs}. Dữ liệu này cho thấy bạn có đủ điều kiện cơ sở để tiếp cận chuyên ngành **{major_name}**."
        else:
            gpa_cmt = f"Mức điểm **{top_s_names} ({max_gpa})** là một chỉ số ưu tú trong hồ sơ của bạn. Cấp độ này minh chứng cho {top_s_attrs} sắc bén, tạo lợi thế cạnh tranh rất lớn khi bạn theo học ngành **{major_name}**."

    explanation = f"**🧠 Phân tích Tâm lý học:**\n{holland_cmt}\n\n**📊 Phân tích Học thuật:**\n{gpa_cmt}"
    return explanation


# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="FlowATS – AI Tư Vấn Ngành Học",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. CSS HIỆN ĐẠI ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">

<style>
/* ── Base ─────────────────────────────────────────── */
html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    background-color: #f0f2f8 !important;
    color: #1a1f36;
}

/* ── Sidebar ──────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d1b3e 0%, #162952 60%, #1e3a6e 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: #c8d6f0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

.sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 0 18px;
}
.sidebar-logo-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: linear-gradient(135deg, #4f8ef7, #a78bfa);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.sidebar-logo-text { font-family: 'Sora', sans-serif; font-size: 20px; font-weight: 700; color: #fff !important; }
.sidebar-logo-sub  { font-size: 11px; color: #8ba3cc !important; letter-spacing: .5px; }

.sidebar-badge {
    background: rgba(79,142,247,0.15); border: 1px solid rgba(79,142,247,0.3);
    border-radius: 8px; padding: 10px 14px; margin: 8px 0; font-size: 13px;
}
.sidebar-badge .label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #7aa3d9 !important; margin-bottom: 4px; }
.sidebar-badge .value { font-weight: 600; color: #e0eaff !important; }

/* ── Main header ──────────────────────────────────── */
.hero-wrap {
    text-align: center; padding: 48px 20px 36px; position: relative;
}
.hero-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(79,142,247,.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-chip {
    display: inline-block; background: rgba(79,142,247,.12);
    border: 1px solid rgba(79,142,247,.35); border-radius: 100px;
    padding: 4px 16px; font-size: 12px; font-weight: 500;
    color: #4f8ef7; letter-spacing: .8px; text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: clamp(28px, 4vw, 48px); font-weight: 800;
    color: #0d1b3e; line-height: 1.15; margin: 0 0 14px;
}
.hero-title span { color: #4f8ef7; }
.hero-sub {
    font-size: 16px; color: #6b7a9d; max-width: 560px;
    margin: 0 auto; line-height: 1.65;
}

/* ── Section headers ──────────────────────────────── */
.section-label {
    font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px; color: #4f8ef7;
    margin-bottom: 6px;
}
.section-title {
    font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 700;
    color: #0d1b3e; margin-bottom: 20px;
}

/* ── Cards ────────────────────────────────────────── */
.card {
    background: #ffffff; border-radius: 16px; padding: 28px;
    border: 1px solid #e4e9f4;
    box-shadow: 0 2px 12px rgba(13,27,62,.06);
    margin-bottom: 20px; transition: box-shadow .2s;
}
.card:hover { box-shadow: 0 6px 24px rgba(13,27,62,.10); }

/* ── Submit button ────────────────────────────────── */
.stForm [data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #2563eb 0%, #4f8ef7 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-family: 'Sora', sans-serif !important;
    font-size: 15px !important; font-weight: 600 !important;
    letter-spacing: .5px !important; padding: 14px 24px !important;
    width: 100% !important; cursor: pointer !important;
    box-shadow: 0 4px 16px rgba(37,99,235,.35) !important;
    transition: all .2s !important;
}
.stForm [data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(37,99,235,.45) !important;
}

/* ── Number inputs & sliders ──────────────────────── */
[data-testid="stNumberInput"] input {
    border-radius: 10px !important; border: 1.5px solid #dce3f3 !important;
    background: #f8faff !important; font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important; font-size: 15px !important; color: #0d1b3e !important;
    transition: border-color .2s !important;
}
[data-testid="stNumberInput"] input:focus { border-color: #4f8ef7 !important; }

[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,.2) !important;
}

/* ── Result card ──────────────────────────────────── */
.result-hero {
    background: linear-gradient(135deg, #0d1b3e 0%, #1e3870 50%, #162952 100%);
    border-radius: 20px; padding: 40px 32px; text-align: center;
    position: relative; overflow: hidden; margin-bottom: 20px;
    box-shadow: 0 12px 40px rgba(13,27,62,.25);
}
.result-hero::before {
    content: ''; position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.result-hero::after {
    content: ''; position: absolute;
    top: -60px; right: -60px; width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(79,142,247,.25) 0%, transparent 70%);
}
.result-hero-label {
    font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
    color: rgba(200,214,240,.7); margin-bottom: 12px; position: relative; z-index: 2;
}
.result-hero-major {
    font-family: 'Sora', sans-serif; font-size: clamp(22px, 3vw, 34px);
    font-weight: 800; color: #ffd166; line-height: 1.2;
    text-shadow: 0 2px 8px rgba(0,0,0,.3); position: relative; z-index: 2;
    margin-bottom: 16px;
}
.result-hero-badge {
    display: inline-block; background: rgba(255,209,102,.15);
    border: 1px solid rgba(255,209,102,.4); border-radius: 100px;
    padding: 5px 16px; font-size: 12px; font-weight: 500;
    color: #ffd166; position: relative; z-index: 2;
}

/* ── Insight card ─────────────────────────────────── */
.insight-card {
    background: #f8faff; border-radius: 14px; padding: 20px 22px;
    border: 1px solid #e4e9f4; margin-bottom: 16px;
}
.insight-card-title {
    font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600;
    color: #4f8ef7; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
}

/* ── Top 3 probability bars ───────────────────────── */
.prob-bar-wrap { margin-bottom: 12px; }
.prob-bar-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 6px;
}
.prob-bar-name { font-size: 14px; font-weight: 500; color: #1a1f36; }
.prob-bar-pct  { font-family: 'Sora', sans-serif; font-size: 14px; font-weight: 700; color: #2563eb; }
.prob-bar-track {
    height: 8px; background: #e8edf6; border-radius: 100px; overflow: hidden;
}
.prob-bar-fill {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #2563eb, #60a5fa);
    transition: width .8s cubic-bezier(.4,0,.2,1);
}

/* ── University cards ─────────────────────────────── */
.uni-card {
    background: #fff; border-radius: 12px; padding: 14px 16px;
    border: 1px solid #e4e9f4; margin-bottom: 10px;
    transition: transform .15s, box-shadow .15s;
}
.uni-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(13,27,62,.1); }
.uni-card-name { font-weight: 600; font-size: 14px; color: #0d1b3e; margin-bottom: 4px; }
.uni-card-meta { font-size: 12px; color: #7b8ab0; }
.uni-card-score { font-weight: 700; color: #0d1b3e; }

.uni-col-header {
    border-radius: 12px; padding: 14px 18px; margin-bottom: 14px; text-align: center;
}
.uni-col-title { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 700; }
.uni-col-sub   { font-size: 12px; margin-top: 2px; opacity: .8; }

/* ── Divider ──────────────────────────────────────── */
.fancy-divider {
    display: flex; align-items: center; gap: 16px; margin: 36px 0 28px;
}
.fancy-divider hr { flex: 1; border: none; border-top: 1px solid #dce3f3; }
.fancy-divider-text {
    font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 600;
    color: #9aa8cc; text-transform: uppercase; letter-spacing: 1.5px; white-space: nowrap;
}

/* ── Utility ──────────────────────────────────────── */
.mt-0 { margin-top: 0 !important; }
.stSpinner > div { border-top-color: #4f8ef7 !important; }
</style>
""", unsafe_allow_html=True)


# --- 4. LOAD DATA ---
@st.cache_resource
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model         = joblib.load(os.path.join(base_dir, 'saved_models', 'best_model.pkl'))
    scaler        = joblib.load(os.path.join(base_dir, 'saved_models', 'scaler.pkl'))
    label_encoder = joblib.load(os.path.join(base_dir, 'saved_models', 'label_encoder.pkl'))
    return model, scaler, label_encoder

@st.cache_data
def load_university_data():
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, 'phan_loai_truong.xlsx')
    if os.path.exists(excel_path):
        return pd.read_excel(excel_path)
    return None

try:
    rf_model, scaler, label_encoder = load_models()
    df_uni = load_university_data()
except Exception as e:
    st.error(f"⚠️ Sự cố khi tải dữ liệu hệ thống: {e}")
    st.stop()


# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🎓</div>
        <div>
            <div class="sidebar-logo-text">FlowATS</div>
            <div class="sidebar-logo-sub">AI EDUCATION ADVISOR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Kiến trúc hệ thống**")

    st.markdown("""
    <div class="sidebar-badge">
        <div class="label">Tầng phân tích</div>
        <div class="value">🤖 Random Forest (AI)</div>
    </div>
    <div class="sidebar-badge">
        <div class="label">Tầng diễn giải</div>
        <div class="value">⚙️ Rule-based Engine (XAI)</div>
    </div>
    <div class="sidebar-badge">
        <div class="label">Mô hình tâm lý</div>
        <div class="value">🧬 Holland RIASEC Theory</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("📍 Sản phẩm nghiên cứu của nhóm sinh viên FPT University.")
    st.caption("Phiên bản Beta · 2025")


# --- 6. HERO HEADER ---
st.markdown("""
<div class="hero-wrap">
    <div class="hero-chip">✦ Powered by Machine Learning & Holland Theory</div>
    <h1 class="hero-title">Phân Tích &amp; Tư Vấn<br><span>Ngành Học Phù Hợp</span></h1>
    <p class="hero-sub">Hệ thống kết hợp dữ liệu học thuật và trắc nghiệm tâm lý Holland để đề xuất con đường phù hợp nhất với bạn.</p>
</div>
""", unsafe_allow_html=True)


# --- 7. MAIN LAYOUT ---
col_input, col_result = st.columns([1.15, 1], gap="large")

with col_input:
    with st.form("user_input_form"):

        # — GPA Block —
        st.markdown('<div class="section-label">Bước 01</div><div class="section-title">Năng lực học thuật – GPA lớp 12</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        math = c1.number_input("📐 Toán học",  min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        phy  = c2.number_input("⚡ Vật lý",    min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        chem = c3.number_input("🧪 Hóa học",   min_value=0.0, max_value=10.0, value=7.5, step=0.1)
        c4, c5, _ = st.columns(3)
        lit  = c4.number_input("📖 Ngữ văn",   min_value=0.0, max_value=10.0, value=6.5, step=0.1)
        eng  = c5.number_input("🌐 Tiếng Anh", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

        # — Holland Block —
        st.markdown('<div class="section-label">Bước 02</div><div class="section-title">Trắc nghiệm Tâm lý Holland</div>', unsafe_allow_html=True)
        st.caption("Đánh giá từ **1** (Hoàn toàn không phù hợp) đến **5** (Hoàn toàn phù hợp)")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

        h1, h2, h3 = st.columns(3)
        R = h1.slider("🔧 R · Kỹ thuật",     1, 5, 4)
        I = h2.slider("🔬 I · Nghiên cứu",   1, 5, 4)
        A = h3.slider("🎨 A · Nghệ thuật",   1, 5, 2)
        h4, h5, h6 = st.columns(3)
        S = h4.slider("🤝 S · Xã hội",       1, 5, 3)
        E = h5.slider("📈 E · Quản lý",      1, 5, 3)
        C = h6.slider("📋 C · Tổ chức",      1, 5, 3)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        submit = st.form_submit_button("🚀 TIẾN HÀNH PHÂN TÍCH", use_container_width=True)


# --- 8. RESULT PANEL ---
with col_result:
    if not submit:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg,#f0f4ff,#e8eeff);
            border: 1.5px dashed #c3ceee; border-radius: 20px;
            padding: 60px 32px; text-align: center; margin-top: 4px;
        ">
            <div style="font-size:56px; margin-bottom:16px;">🎯</div>
            <div style="font-family:'Sora',sans-serif; font-size:18px; font-weight:700; color:#0d1b3e; margin-bottom:10px;">
                Kết quả sẽ hiển thị tại đây
            </div>
            <div style="font-size:14px; color:#7b8ab0; line-height:1.6;">
                Điền đầy đủ thông tin bên trái<br>và nhấn nút phân tích để xem kết quả.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Hệ thống đang phân tích dữ liệu…"):
            user_input  = np.array([[math, phy, chem, lit, eng, R, I, A, S, E, C]])
            user_scaled = scaler.transform(user_input)

            all_probs      = rf_model.predict_proba(user_scaled)[0]
            top3_idx       = np.argsort(all_probs)[-3:][::-1]
            top3_majors    = label_encoder.inverse_transform(top3_idx)
            top3_probs_raw = all_probs[top3_idx]

            boosted     = top3_probs_raw ** 2
            top3_pcts   = (boosted / boosted.sum()) * 100
            best_major  = top3_majors[0]

        # Hero result card
        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-label">⭐ Chuyên ngành đề xuất tối ưu</div>
            <div class="result-hero-major">{best_major.upper()}</div>
            <div class="result-hero-badge">✦ Kết quả phân tích AI</div>
        </div>
        """, unsafe_allow_html=True)

        # Top 3 probability bars
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown('<div class="insight-card-title">📊 Mức độ tương thích – Top 3</div>', unsafe_allow_html=True)
        colors = ["#2563eb", "#60a5fa", "#bfdbfe"]
        for i, (major, pct) in enumerate(zip(top3_majors, top3_pcts)):
            rank_icon = ["🥇", "🥈", "🥉"][i]
            st.markdown(f"""
            <div class="prob-bar-wrap">
                <div class="prob-bar-header">
                    <div class="prob-bar-name">{rank_icon} {major}</div>
                    <div class="prob-bar-pct">{pct:.1f}%</div>
                </div>
                <div class="prob-bar-track">
                    <div class="prob-bar-fill" style="width:{pct:.1f}%; background: linear-gradient(90deg, {colors[i]}, {colors[i]}88);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Explanation
        user_gpa     = {'Toán': math, 'Lý': phy, 'Hóa': chem, 'Văn': lit, 'Anh': eng}
        user_holland = {'Holland_R': R, 'Holland_I': I, 'Holland_A': A, 'Holland_S': S, 'Holland_E': E, 'Holland_C': C}
        explanation  = generate_explanation(user_gpa, user_holland, best_major)

        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown('<div class="insight-card-title">📋 Báo cáo phân tích</div>', unsafe_allow_html=True)
        st.markdown(explanation)
        st.markdown('</div>', unsafe_allow_html=True)


# --- 9. UNIVERSITY SECTION ---
if submit and df_uni is not None:
    st.markdown(f"""
    <div class="fancy-divider">
        <hr/><div class="fancy-divider-text">🏫 Tham chiếu phổ điểm đại học · {best_major.upper()}</div><hr/>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="text-align:center; color:#7b8ab0; margin-bottom:28px; font-size:14px;">
        Dữ liệu được phân cụm theo ngưỡng điểm chuẩn thực tế để hỗ trợ chiến lược nộp hồ sơ ngành <strong>{best_major}</strong>.
    </p>
    """, unsafe_allow_html=True)

    df_filtered = df_uni[df_uni['Nganh_Hoc'] == best_major]

    if not df_filtered.empty:
        col_top, col_mid, col_safe = st.columns(3, gap="medium")

        groups = [
            (col_top,  'Top',  '#ef4444', '🔴', 'Nhóm Cạnh Tranh',  'Yêu cầu năng lực xuất sắc',   '#fff5f5', '#fecaca'),
            (col_mid,  'Mid',  '#f59e0b', '🟡', 'Nhóm Tiêu Chuẩn',  'Yêu cầu năng lực khá – giỏi', '#fffbeb', '#fde68a'),
            (col_safe, 'Safe', '#10b981', '🟢', 'Nhóm An Toàn',      'Tỷ lệ trúng tuyển cao',       '#f0fdf4', '#a7f3d0'),
        ]

        for col, key, color, icon, title, sub, bg, border in groups:
            with col:
                st.markdown(f"""
                <div class="uni-col-header" style="background:{bg}; border:1px solid {border};">
                    <div class="uni-col-title" style="color:{color};">{icon} {title}</div>
                    <div class="uni-col-sub"   style="color:{color};">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

                schools = df_filtered[df_filtered['Phan_Loai_Truong'] == key]
                for _, row in schools.iterrows():
                    st.markdown(f"""
                    <div class="uni-card" style="border-left: 3px solid {color};">
                        <div class="uni-card-name">{row['Ten_Truong']}</div>
                        <div class="uni-card-meta">
                            Tổ hợp: {row['To_Hop_Mon']} &nbsp;·&nbsp;
                            Điểm chuẩn: <span class="uni-card-score">{row['Diem_Chuan']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info(f"🔄 Hệ thống đang đồng bộ hóa dữ liệu phổ điểm cho ngành **{best_major}**.")
