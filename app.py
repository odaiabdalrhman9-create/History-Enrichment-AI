import streamlit as st

# إعداد الصفحة لتكون واسعة وتدعم التنسيق
st.set_page_config(page_title="مولد إثراء التاريخ", layout="wide")

# كود CSS لتجميل الواجهة والبطاقات
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stApp {color: white;}
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: #1e2530;
        border: 1px solid #333;
        margin: 10px;
        text-align: center;
        min-height: 180px;
    }
    .footer {text-align: center; margin-top: 50px; color: #888; font-size: 0.9em;}
    </style>
""", unsafe_allow_html=True)

# الواجهة العربية
st.title("مولد إثراء التاريخ")
st.subheader("ستوديو تصميم الذكاء الاصطناعي - عقول غاردنر الخمسة")
st.write("توليد أنشطة إثراء تاريخي متعددة الأوجه لمنهج المطور: **عدي عبد الرحمن**")

# المدخلات
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("أدخل الموضوع التاريخي:")
with col2:
    age_group = st.selectbox("اختر المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

if st.button("توليد النشاط"):
    if topic:
        st.success(f"جاري تصميم الأنشطة للمرحلة الـ {age_group} حول: {topic}")
        
        # تقسيم البطاقات مع التعديلات التربوية
        cols = st.columns(5)
        minds = ["المنضبط", "المركب", "المبدع", "المحترم", "الأخلاقي"]
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div class='card'><b>العقل {minds[i]}</b><br><br>...جارِ التوليد...</div>", unsafe_allow_html=True)
    else:
        st.warning("يرجى إدخال موضوع أولاً!")

# التذييل
st.markdown("<div class='footer'>المطور: عدي عبد الرحمن</div>", unsafe_allow_html=True)
