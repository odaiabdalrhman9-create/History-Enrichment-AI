import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مصمم الأنشطة الإثرائية الذكي", layout="centered", page_icon="⚡")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY.")
    st.stop()

# تصميم مفعم بالحيوية (ألوان زرقاء وتركوازية)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    .main-header {
        color: #ffffff; 
        text-align: center; 
        font-family: 'Segoe UI', sans-serif;
        padding: 20px;
        margin-bottom: 20px;
    }
    .activity-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        border-left: 5px solid #00d2ff;
        color: #1e293b;
    }
    .footer {
        text-align: center; 
        margin-top: 80px; 
        padding: 20px; 
        color: #cbd5e1; 
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<h1 class='main-header'>⚡ مصمم الأنشطة الإثرائية الذكي</h1>", unsafe_allow_html=True)

# المدخلات
lesson_name = st.text_input("💡 اسم الدرس أو الموضوع:", placeholder="مثلاً: التمثيل الضوئي، التفاعلات الكيميائية، العصور التاريخية...")
grade_level = st.select_slider("🎓 المرحلة الدراسية:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if st.button("🚀 توليد الأنشطة", type="primary"):
    if not lesson_name:
        st.warning("⚠️ يرجى إدخال اسم الدرس أولاً.")
    else:
        with st.spinner("جاري تصميم الأنشطة الإثرائية..."):
            prompt = f"""
            بصفتك خبيراً في المناهج وطرائق التدريس، صمم 3 أنشطة إثرائية إبداعية للدرس: '{lesson_name}'، للمرحلة '{grade_level}'.
            1. نشاط استكشافي (يحفز الفضول).
            2. نشاط تطبيقي (يعتمد على الممارسة والتحليل).
            3. نشاط تقييمي إبداعي (بعيداً عن الأنماط التقليدية).
            لكل نشاط، حدد: الهدف التربوي، خطوات التنفيذ، والأدوات.
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            
            st.markdown("<div class='activity-card'>" + response.choices[0].message.content + "</div>", unsafe_allow_html=True)

# الفوتر
st.markdown("""
    <div class='footer'>
        تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓
    </div>
""", unsafe_allow_html=True)
