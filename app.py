import streamlit as st
from groq import Groq

# إعداد الصفحة لتكون واسعة
st.set_page_config(page_title="مولد إثراء التاريخ", layout="wide")

# إعداد مفتاح API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# كود CSS
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

st.title("مولد إثراء التاريخ")
st.subheader("ستوديو تصميم الذكاء الاصطناعي - عقول غاردنر الخمسة")
st.write("""توليد أنشطة إثراء تاريخي متعددة الأوجه للمطور: عدي عبد الرحمن""")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("أدخل الموضوع التاريخي:")
with col2:
    age_group = st.selectbox("اختر المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

if st.button("توليد النشاط"):
    if topic:
        with st.spinner("جاري تصميم الأنشطة..."):
            prompt = (
                f"صمم 5 أنشطة تعليمية تاريخية حول {topic} للمرحلة {age_group} "
                "بناءً على عقول غاردنر الخمسة (المنضبط، المركب، المبدع، المحترم، الأخلاقي). "
                "أجب باختصار في 5 فقرات منفصلة."
            )
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            response = chat_completion.choices[0].message.content
            activities = response.split('\n\n')

        cols = st.columns(5)
        minds = ["المنضبط", "المركب", "المبدع", "المحترم", "الأخلاقي"]
        
        for i, col in enumerate(cols):
            with col:
                content = activities[i] if i < len(activities) else "جارِ التجهيز..."
                st.markdown(f"<div class='card'><b>العقل {minds[i]}</b><br><br>{content}</div>", unsafe_allow_html=True)
    else:
        st.warning("يرجى إدخال موضوع أولاً!")

st.markdown("<div class='footer'>المطور: عدي عبد الرحمن</div>", unsafe_allow_html=True)
