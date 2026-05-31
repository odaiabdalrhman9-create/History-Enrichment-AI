import streamlit as st
import json
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مصمم الأنشطة الإثرائي الذكي", layout="wide", page_icon="⚡")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY.")
    st.stop()

# تصميم الواجهة الاحترافية (CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    .main-header { color: #ffffff; text-align: center; margin-bottom: 30px; }
    .box-goal { background: #e0f7fa; padding: 15px; border-radius: 10px; color: #006064; height: 100%; }
    .box-steps { background: #e8f5e9; padding: 15px; border-radius: 10px; color: #1b5e20; height: 100%; }
    .box-tools { background: #f5f5f5; padding: 15px; border-radius: 10px; color: #424242; height: 100%; }
    .footer { text-align: center; margin-top: 50px; color: #cbd5e1; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>⚡ مصمم الأنشطة الإثرائية الذكي</h1>", unsafe_allow_html=True)

# المدخلات
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    lesson_name = st.text_input("💡 اسم الدرس:", placeholder="مثال: الدولة العباسية")
with col_in2:
    grade_level = st.select_slider("🎓 المرحلة:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if 'data' not in st.session_state: st.session_state.data = None

if st.button("🚀 توليد الأنشطة الإثرائية", type="primary"):
    with st.spinner("جاري صياغة الأنشطة..."):
        prompt = f"""
        صمم 3 أنشطة إثرائية لدرس '{lesson_name}' للمرحلة '{grade_level}'.
        أخرج النتيجة حصراً بصيغة JSON التالية:
        {{
            "نشاط1": {{"الهدف": "...", "الخطوات": "...", "الأدوات": "..."}},
            "نشاط2": {{"الهدف": "...", "الخطوات": "...", "الأدوات": "..."}},
            "نشاط3": {{"الهدف": "...", "الخطوات": "...", "الأدوات": "..."}}
        }}
        """
        try:
            res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            content = res.choices[0].message.content.replace("```json", "").replace("
```", "")
            st.session_state.data = json.loads(content)
        except:
            st.error("حدث خطأ في توليد المحتوى. حاول مجدداً.")

# عرض النتائج في Tabs بتنسيق أفقي
if st.session_state.data:
    tabs = st.tabs(["نشاط 1", "نشاط 2", "نشاط 3"])
    for i, tab in enumerate(tabs):
        with tab:
            act = st.session_state.data[f"نشاط{i+1}"]
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f"<div class='box-goal'><b>🎯 الهدف:</b><br>{act['الهدف']}</div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='box-steps'><b>📋 الخطوات:</b><br>{act['الخطوات']}</div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='box-tools'><b>🛠 الأدوات:</b><br>{act['الأدوات']}</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓</div>", unsafe_allow_html=True)
