import streamlit as st
from groq import Groq
import time

# إعداد الصفحة
st.set_page_config(page_title="مصمم الأنشطة الإثرائية الذكي", layout="centered", page_icon="⚡")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في الإعدادات.")
    st.stop()

# التصميم المحدث (CSS متقدم)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    .main-header { color: #ffffff !important; text-align: center; margin-bottom: 30px; }
    .stTextInput label, .stSlider label { color: #ffffff !important; font-weight: bold !important; }
    .activity-card { background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; border-left: 5px solid #00d2ff; color: #334155; }
    .footer { text-align: center; margin-top: 50px; color: #cbd5e1; }
    </style>
""", unsafe_allow_html=True)

# إدارة الحالة (Session Persistence)
if 'result' not in st.session_state: st.session_state.result = None

st.markdown("<h1 class='main-header'>⚡ مصمم الأنشطة الإثرائية الذكي</h1>", unsafe_allow_html=True)

# المدخلات مع تحسين المساحات
lesson_name = st.text_input("💡 اسم الدرس أو الموضوع:", placeholder="مثلاً: التفاعلات الكيميائية...")
st.markdown("*(نصيحة: كلما كنت محدداً في اسم الدرس، كانت الأنشطة أكثر إبداعاً)*")
st.markdown("<br>", unsafe_allow_html=True)
grade_level = st.select_slider("🎓 المرحلة الدراسية:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])
goal_context = st.text_input("🎯 الهدف من النشاط (اختياري):", placeholder="مثلاً: تعزيز العمل الجماعي..")

if st.button("🚀 توليد الأنشطة الإثرائية", type="primary"):
    if not lesson_name:
        st.warning("⚠️ يرجى إدخال اسم الدرس!")
    else:
        # مؤشر تقدم احترافي
        progress_text = "جاري هندسة الأنشطة التعليمية..."
        bar = st.progress(0, text=progress_text)
        
        try:
            prompt = f"""
            بصفتك خبير مناهج، صمم 3 أنشطة إثرائية للدرس '{lesson_name}' للمرحلة '{grade_level}'.
            السياق الإضافي: {goal_context if goal_context else 'لا يوجد'}
            التنسيق الإجباري:
            1. ابدأ كل نشاط بعنوان واضح.
            2. استخدم التنسيق التالي لكل نشاط: **الهدف التربوي**، **خطوات التنفيذ**، **الأدوات**.
            3. استخدم Markdown للخط العريض ولا تستخدم أي كلمات إنجليزية.
            4. اجعل الأنشطة منظمة ومهنية.
            """
            
            res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            st.session_state.result = res.choices[0].message.content
            bar.progress(100, text="اكتملت المهمة!")
        except Exception as e:
            st.error("حدث خطأ تقني، يرجى المحاولة لاحقاً.")

# عرض النتائج في Tabs إذا توفرت
if st.session_state.result:
    st.markdown("---")
    # تقسيم النتيجة لـ 3 تبويبات (هنا نفترض الفصل بناءً على الترقيم)
    tab1, tab2, tab3 = st.tabs(["نشاط 1", "نشاط 2", "نشاط 3"])
    
    # تبسيط: سنعرض النتيجة كاملة في كل تبويب أو نقوم بمعالجتها
    with tab1: st.markdown(f"<div class='activity-card'>{st.session_state.result.split('2.')[0]}</div>", unsafe_allow_html=True)
    with tab2: st.markdown(f"<div class='activity-card'>نشاط 2: " + st.session_state.result.split('2.')[1].split('3.')[0] + "</div>", unsafe_allow_html=True)
    with tab3: st.markdown(f"<div class='activity-card'>نشاط 3: " + st.session_state.result.split('3.')[1] + "</div>", unsafe_allow_html=True)
    
    st.button("نسخ النتائج", on_click=lambda: st.write("تم النسخ! (تجريبي)"))

# الفوتر
st.markdown("""
    <div class='footer'>
        تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓
    </div>
""", unsafe_allow_html=True)
