import streamlit as st
from groq import Groq
from fpdf import FPDF

# إعداد الصفحة
st.set_page_config(page_title="مختبر العقول الخمسة", layout="wide")

# إعداد Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في الـ Secrets.")
    st.stop()

# التنسيق البصري (تصميم تعليمي هادئ)
st.markdown("""
    <style>
    .stApp {background-color: #f8f9fa;}
    .card {padding: 20px; border-radius: 10px; background-color: #ffffff; border-left: 5px solid #0056b3; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px;}
    .title-box {text-align: center; color: #0056b3; margin-bottom: 30px;}
    .footer {text-align: center; margin-top: 50px; color: #6c757d;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-box'><h1>مختبر العقول الخمسة</h1><p>تصميم استراتيجيات التعلم التاريخي</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
topic = col1.text_input("الموضوع التاريخي:")
age_group = col2.selectbox("المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

if st.button("توليد الخارطة التعليمية"):
    if topic:
        with st.spinner("جاري بناء الأنشطة التربوية..."):
            prompt = (f"صمم خارطة طريق تعليمية للمرحلة {age_group} حول {topic} بناءً على نظرية هوارد غاردنر للعقول الخمسة. "
                      "لكل عقل (المنضبط، المركب، المبدع، المحترم، الأخلاقي) حدد: 1. الهدف التربوي 2. النشاط التفاعلي 3. أداة التقييم. "
                      "يجب أن تكون الإجابة مفصلة ومهنية.")
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            res_text = response.choices[0].message.content
            st.session_state['result'] = res_text
            st.markdown(f"<div class='card'>{res_text}</div>", unsafe_allow_html=True)
            
            # ميزة التصدير لـ PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Strategy for: {topic}", ln=True, align='C')
            pdf.multi_cell(0, 10, txt=res_text.encode('latin-1', 'replace').decode('latin-1'))
            pdf_output = "history_plan.pdf"
            pdf.output(pdf_output)
            with open(pdf_output, "rb") as f:
                st.download_button("تحميل الخطة كـ PDF", f, file_name="history_plan.pdf")
    else:
        st.warning("أدخل موضوعاً للبدء!")

st.markdown("<div class='footer'>المطور: عدي عبد الرحمن</div>", unsafe_allow_html=True)
