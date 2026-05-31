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

# تصميم CSS مُحسن
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    .main-header { color: #ffffff; text-align: center; margin-bottom: 30px; }
    .box { padding: 20px; border-radius: 15px; height: 100%; color: #ffffff; margin-bottom: 10px; line-height: 1.6; }
    .box-goal { background: #0891b2; } 
    .box-steps { background: #059669; } 
    .box-tools { background: #7c3aed; } 
    .footer { text-align: center; margin-top: 50px; color: #cbd5e1; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>⚡ مصمم الأنشطة الإثرائية الذكي</h1>", unsafe_allow_html=True)

# المدخلات
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    lesson_name = st.text_input("💡 اسم الدرس:", placeholder="مثال: تاريخ الدولة المملوكية")
with col_in2:
    grade_level = st.select_slider("🎓 المرحلة:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if 'data' not in st.session_state: st.session_state.data = None

if st.button("🚀 توليد الأنشطة الإثرائية", type="primary"):
    with st.spinner("جاري صياغة الأنشطة..."):
        prompt = f"""
        صمم 3 أنشطة إثرائية لدرس '{lesson_name}' للمرحلة '{grade_level}'.
        أخرج النتيجة بتنسيق JSON فقط.
        القيم داخل "الخطوات" يجب أن تكون نصاً يحتوي على أرقام وتسلسل عمودي باستخدام '\\n'.
        {{
            "نشاط1": {{"الهدف": "...", "الخطوات": "1. ...\n2. ...\n3. ...", "الأدوات": "..."}},
            "نشاط2": {{"الهدف": "...", "الخطوات": "1. ...\n2. ...\n3. ...", "الأدوات": "..."}},
            "نشاط3": {{"الهدف": "...", "الخطوات": "1. ...\n2. ...\n3. ...", "الأدوات": "..."}}
        }}
        """
        try:
            res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            content = res.choices[0].message.content.replace("```json", "").replace("
```", "").strip()
            # إزالة رموز التحكم غير المرئية لمنع خطأ JSON
            content = re.sub(r'[\x00-\x1f]', '', content)
            st.session_state.data = json.loads(content)
        except Exception as e:
            st.error(f"حدث خطأ في معالجة البيانات: {e}")

# عرض النتائج في Tabs
if st.session_state.data:
    tabs = st.tabs(["💡 نشاط 1", "💡 نشاط 2", "💡 نشاط 3"])
    
    for i, tab in enumerate(tabs):
        with tab:
            key = f"نشاط{i+1}"
            if key in st.session_state.data:
                act = st.session_state.data[key]
                c1, c2, c3 = st.columns(3)
                
                with c1: st.markdown(f"<div class='box box-goal'><b>🎯 الهدف:</b><br>{act.get('الهدف', '')}</div>", unsafe_allow_html=True)
                # استبدال \n بـ <br> لضمان ظهور الخطوات بشكل عمودي
                steps_formatted = act.get('الخطوات', '').replace('\n', '<br>')
                with c2: st.markdown(f"<div class='box box-steps'><b>📋 الخطوات:</b><br>{steps_formatted}</div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='box box-tools'><b>🛠 الأدوات:</b><br>{act.get('الأدوات', '')}</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓</div>", unsafe_allow_html=True)
