import streamlit as st
from groq import Groq

# إعداد الصفحة لتكون واسعة
st.set_page_config(page_title="مولد إثراء التاريخ", layout="wide")

# إعداد مفتاح API من الإعدادات الآمنة (Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# كود CSS لتجميل الواجهة والبطاقات
st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color: white;}
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: #1e2530;
        border: 1px solid #333;
        margin: 10px;
        text-align: center;
        min-height: 250px;
        color: white;
    }
    .footer { text-align: center; margin-top: 50px; color: #888; font-size: 0.9em; }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.title("مولد إثراء التاريخ")
st.subheader("ستوديو تصميم الذكاء الاصطناعي - عقول غاردنر الخمسة")
st.write("توليد أنشطة إثراء تاريخي متعددة الأوجه للمطور: **عدي عبد الرحمن**")

# المدخلات
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("أدخل الموضوع التاريخي:")
with col2:
    age_group = st.selectbox("اختر المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

if st.button("توليد النشاط"):
    if topic:
        with st.spinner("جاري تصميم الأنشطة بواسطة الذكاء الاصطناعي..."):
            # طلب من Groq
            prompt = f"صمم 5 أنشطة تعليمية تاريخية حول {topic} للمرحلة {age_group} بناءً
