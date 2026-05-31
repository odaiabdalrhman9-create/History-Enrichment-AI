import streamlit as st
from groq import Groq

# إعداد الصفحة بواجهة احترافية
st.set_page_config(page_title="مصمم الأنشطة الذكي", layout="centered", page_icon="🧩")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY.")
    st.stop()

# تصميم احترافي (Professional & Minimalist)
st.markdown("""
    <style>
    .main-header {color: #1e293b; text-align: center; font-family: 'Segoe UI', sans-serif; margin-bottom: 30px;}
    .footer {text-align: center; margin-top: 100px; padding: 20px; color: #64748b; font-size: 0.9em; border-top: 1px solid #e2e8f0;}
    .activity-box {background: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<h1 class='main-header'>🧩 مصمم الأنشطة الذكي</h1>", unsafe_allow_html=True)

# المدخلات
lesson_name = st.text_input("أدخل اسم الدرس أو الموضوع:", placeholder="مثال: التفاعل الكيميائي، الدولة الأموية، نظرية فيثاغورس...")
grade_level = st.select_slider("حدد المرحلة الدراسية (اختياري):", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if st.button("توليد الأنشطة", type="primary"):
    if not lesson_name:
        st.warning("يرجى إدخال اسم الدرس أولاً.")
    else:
        with st.spinner("جاري تحليل المحتوى وتصميم الأنشطة..."):
            prompt = f"""
            بصفتك مصمماً تعليمياً خبيراً، صمم 3 أنشطة تعليمية متنوعة للدرس التالي: '{lesson_name}'، بما يناسب المرحلة '{grade_level}'.
            يجب أن تكون الأنشطة:
            1. نشاط استكشافي (يحفز الفضول المعرفي).
            2. نشاط تطبيقي (يعتمد على الممارسة العملية والتحليل).
            3. نشاط تقييمي إبداعي (بعيداً عن الاختبارات التقليدية).
            
            لكل نشاط، حدد بوضوح: (الهدف التربوي، خطوات التنفيذ، الأدوات المطلوبة).
            اجعل المخرجات منظمة باحترافية، وكن مبتكراً في الأفكار.
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            
            st.markdown("<div class='activity-box'>" + response.choices[0].message.content + "</div>", unsafe_allow_html=True)

# الفوتر الاحترافي
st.markdown("""
    <div class='footer'>
        تطوير: <b>عدي عبد الرحمن</b> <br>
        ماجستير في المناهج وطرائق التدريس
    </div>
""", unsafe_allow_html=True)
