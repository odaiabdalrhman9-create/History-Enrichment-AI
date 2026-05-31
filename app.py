import streamlit as st
from groq import Groq

# إعداد الصفحة بواجهة احترافية
st.set_page_config(page_title="مصمم الأنشطة الذكي", layout="centered", page_icon="🎨")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY.")
    st.stop()

# تصميم مفعم بالألوان (Vibrant UI)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
    }
    .main-header {
        color: #ffffff; 
        text-align: center; 
        font-family: 'Arial', sans-serif; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .activity-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 2px solid white;
        margin-top: 20px;
        color: #333;
    }
    .footer {
        text-align: center; 
        margin-top: 80px; 
        padding: 20px; 
        color: #ffffff; 
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<h1 class='main-header'>🌈 مصمم الأنشطة الذكي</h1>", unsafe_allow_html=True)

# المدخلات
lesson_name = st.text_input("💡 اسم الدرس أو الموضوع:", placeholder="مثلاً: التمثيل الضوئي، الشعر الجاهلي...")
grade_level = st.select_slider("🎓 المرحلة الدراسية:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if st.button("🚀 توليد أنشطة إبداعية", type="primary"):
    if not lesson_name:
        st.warning("⚠️ يرجى إدخال اسم الدرس أولاً.")
    else:
        with st.spinner("✨ جاري الرسم والإبداع..."):
            prompt = f"""
            بصفتك مصمماً تعليمياً خبيراً، صمم 3 أنشطة تعليمية مفعمة بالحيوية للدرس: '{lesson_name}'، للمرحلة '{grade_level}'.
            1. نشاط استكشافي مشوق.
            2. نشاط تطبيقي تفاعلي.
            3. نشاط تقييمي مبتكر وغير تقليدي.
            لكل نشاط، حدد: الهدف، الخطوات، والأدوات.
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            
            st.markdown("<div class='activity-card'>" + response.choices[0].message.content + "</div>", unsafe_allow_html=True)

# الفوتر
st.markdown("""
    <div class='footer'>
        تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎨✨
    </div>
""", unsafe_allow_html=True)
