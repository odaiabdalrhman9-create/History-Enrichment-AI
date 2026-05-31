import streamlit as st
import json
import re
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مصمم الأنشطة الإثرائي الذكي", layout="wide", page_icon="⚡")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في الإعدادات.")
    st.stop()

# تصميم CSS مُحسن لضمان وضوح الألوان
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    
    /* جعل العناوين والمدخلات بيضاء بالكامل */
    h1, .stTextInput label, .stSlider label { color: #ffffff !important; }
    
    .main-header { color: #ffffff; text-align: center; margin-bottom: 30px; }
    
    /* تنسيق التبويبات (Tabs) لتكون بيضاء وواضحة */
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    
    /* مربعات الأنشطة */
    .box { padding: 20px; border-radius: 15px; color: #ffffff; margin-bottom: 10px; line-height: 1.6; border: 1px solid rgba(255,255,255,0.2); }
    .box-goal { background: rgba(8, 145, 178, 0.8); } 
    .box-steps { background: rgba(5, 150, 105, 0.8); } 
    .box-tools { background: rgba(124, 58, 237, 0.8); } 
    
    .footer { text-align: center; margin-top: 50px; color: #ffffff; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>⚡ مصمم الأنشطة الإثرائية الذكي</h1>", unsafe_allow_html=True)

# المدخلات
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    lesson_name = st.text_input("💡 اسم الدرس:", placeholder="مثال: تاريخ الدولة المملوكية")
with col_in2:
    grade_level = st.select_slider("🎓 المرحلة:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if 'data' not in st.session_state: 
    st.session_state.data = None

if st.button("🚀 توليد الأنشطة الإثرائية", type="primary"):
    with st.spinner("جاري صياغة الأنشطة..."):
        prompt = f"""
        صمم 3 أنشطة إثرائية لدرس '{lesson_name}' للمرحلة '{grade_level}'.
        أخرج النتيجة بتنسيق JSON فقط.
        الخطوات يجب أن تكون قائمة مرقمة (1. 2. 3.) مفصولة بعلامة '\\n'.
        {{
            "نشاط1": {{"الهدف": "...", "الخطوات": "1. ...\\n2. ...\\n3. ...", "الأدوات": "..."}},
            "نشاط2": {{"الهدف": "...", "الخطوات": "1. ...\\n2. ...\\n3. ...", "الأدوات": "..."}},
            "نشاط3": {{"الهدف": "...", "الخطوات": "1. ...\\n2. ...\\n3. ...", "الأدوات": "..."}}
        }}
        """
        try:
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}], 
                model="llama-3.3-70b-versatile"
            )
            raw_content = res.choices[0].message.content
            clean_content = raw_content.replace("```json", "").replace("```", "").strip()
            clean_content = re.sub(r'[\x00-\x1f]', '', clean_content)
            st.session_state.data = json.loads(clean_content)
        except Exception as e:
            st.error(f"حدث خطأ في المعالجة: {e}")

# عرض النتائج في Tabs
if st.session_state.data:
    tabs = st.tabs(["💡 نشاط 1", "💡 نشاط 2", "💡 نشاط 3"])
    
    for i, tab in enumerate(tabs):
        with tab:
            key = f"نشاط{i+1}"
            if key in st.session_state.data:
                act = st.session_state.data[key]
                c1, c2, c3 = st.columns(3)
                
                with c1: 
                    st.markdown(f"<div class='box box-goal'><b>🎯 الهدف:</b><br>{act.get('الهدف', '')}</div>", unsafe_allow_html=True)
                with c2: 
                    steps = act.get('الخطوات', '').replace('\n', '<br>')
                    st.markdown(f"<div class='box box-steps'><b>📋 الخطوات:</b><br>{steps}</div>", unsafe_allow_html=True)
                with c3: 
                    st.markdown(f"<div class='box box-tools'><b>🛠 الأدوات:</b><br>{act.get('الأدوات', '')}</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓</div>", unsafe_allow_html=True)
