import streamlit as st
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# إعداد الصفحة
st.set_page_config(page_title="مختبر العقول الخمسة", layout="wide")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في إعدادات Secrets.")
    st.stop()

# التنسيق البصري الاحترافي
st.markdown("""
    <style>
    .stApp {background-color: #f8f9fa;}
    .card {padding: 25px; border-radius: 12px; background-color: #ffffff; border-left: 6px solid #0056b3; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px;}
    .title-box {text-align: center; color: #0056b3; margin-bottom: 40px;}
    .footer {text-align: center; margin-top: 60px; color: #6c757d; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-box'><h1>مختبر العقول الخمسة</h1><p>أداة هندسة المناهج التاريخية</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
topic = col1.text_input("الموضوع التاريخي:")
age_group = col2.selectbox("المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

if st.button("توليد الخارطة التعليمية الاحترافية"):
    if not topic:
        st.warning("يرجى إدخال الموضوع!")
    else:
        with st.spinner("جاري تصميم الخارطة التربوية بدقة..."):
            # هذا هو الـ Prompt الصارم الذي سيجبره على الالتزام بالعقول الخمسة
            prompt = (
                f"بصفتك خبيراً تربوياً، صمم خارطة طريق تعليمية للمرحلة {age_group} حول موضوع '{topic}'. "
                "التزم حصراً بنظرية هوارد غاردنر لـ 'العقول الخمسة للمستقبل' (5 Minds for the Future) وهي: "
                "1. العقل المنضبط (Disciplined Mind) 2. العقل المركب (Synthesizing Mind) 3. العقل المبدع (Creating Mind) 4. العقل المحترم (Respectful Mind) 5. العقل الأخلاقي (Ethical Mind). "
                "لكل عقل، قدم الفقرات التالية فقط: 1. الهدف التربوي 2. النشاط التفاعلي 3. أداة التقييم. "
                "تحذير هام: لا تستخدم الذكاءات المتعددة، ولا العقول اللغوية أو الرياضية أو الموسيقية. التزم فقط بالعقول الخمسة للمستقبل."
            )
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                res_text = response.choices[0].message.content
                st.session_state['result'] = res_text
                
                # عرض النتيجة
                st.markdown(f"<div class='card'>{res_text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# زر التصدير (ملاحظة: يحتاج ملف خطوط لاتقان العربية، هذا كود مبدئي للتصدير)
if 'result' in st.session_state:
    if st.button("تصدير النتائج كملف PDF"):
        pdf_file = "history_plan.pdf"
        c = canvas.Canvas(pdf_file, pagesize=A4)
        c.drawString(100, 800, "خارطة طريق مختبر العقول الخمسة")
        c.drawString(100, 780, f"الموضوع: {topic}")
        c.save()
        with open(pdf_file, "rb") as f:
            st.download_button("اضغط لتحميل الملف", f, file_name="history_plan.pdf")

st.markdown("<div class='footer'>المطور: عدي عبد الرحمن</div>", unsafe_allow_
