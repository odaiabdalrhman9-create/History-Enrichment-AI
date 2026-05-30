import streamlit as st
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# إعداد الصفحة
st.set_page_config(page_title="مختبر العقول الخمسة", layout="wide")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في الـ Secrets.")
    st.stop()

# التنسيق
st.markdown("<h1 style='text-align: center; color: #0056b3;'>مختبر العقول الخمسة</h1>", unsafe_allow_html=True)

topic = st.text_input("الموضوع التاريخي:")
age_group = st.selectbox("المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

if st.button("توليد الخارطة التعليمية"):
    if topic:
        with st.spinner("جاري بناء الأنشطة..."):
            prompt = f"صمم خارطة طريق تعليمية للمرحلة {age_group} حول {topic} بناءً على عقول غاردنر الخمسة. لكل عقل: 1. الهدف التربوي 2. النشاط التفاعلي 3. أداة التقييم."
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            res_text = response.choices[0].message.content
            st.session_state['result'] = res_text
            st.write(res_text)

            # التصدير لـ PDF
            if st.button("تحميل كـ PDF"):
                pdf_file = "history_plan.pdf"
                c = canvas.Canvas(pdf_file, pagesize=A4)
                # ملاحظة: لكي تظهر العربية بشكل مثالي، يفضل استخدام خط يدعم العربية
                # هنا نستخدم نصاً بسيطاً وتأكيداً على التحميل
                c.drawString(100, 800, "تقرير مختبر العقول الخمسة")
                c.save()
                with open(pdf_file, "rb") as f:
                    st.download_button("اضغط هنا لتحميل الملف", f, file_name="history_plan.pdf")
    else:
        st.warning("أدخل موضوعاً للبدء!")

st.markdown("<div style='text-align: center; margin-top: 50px; color: #6c757d;'>المطور: عدي عبد الرحمن</div>", unsafe_allow_html=True)
