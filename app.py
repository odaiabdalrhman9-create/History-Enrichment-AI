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

# تصميم CSS مُحسن لضمان وضوح الألوان
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    .main-header { color: #ffffff; text-align: center; margin-bottom: 30px; }
    /* ألوان واضحة ومتباينة للقراءة */
    .box { padding: 20px; border-radius: 15px; height: 100%; color: #ffffff; margin-bottom: 10px; }
    .box-goal { background: #0284c7; } /* أزرق مشرق */
    .box-steps { background: #059669; } /* أخضر مشرق */
    .box-tools { background: #7c3aed; } /* بنفسجي مشرق */
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
        # تحسين التوجيه ليجبر النموذج على ترتيب الخطوات
        prompt = f"""
        صمم 3 أنشطة إثرائية لدرس '{lesson_name}' للمرحلة '{grade_level}'.
        أخرج النتيجة بتنسيق JSON فقط، وتأكد من أن "الخطوات" عبارة عن نص يحتوي على أرقام (1. 2. 3.) لضمان التسلسل.
        {{
            "نشاط1": {{"الهدف": "...", "الخطوات": "1. ... \n2. ... \n3. ...", "الأدوات": "..."}},
            "نشاط2": {{"الهدف": "...", "الخطوات": "1. ... \n2. ... \n3. ...", "الأدوات": "..."}},
            "نشاط3": {{"الهدف": "...", "الخطوات": "1. ... \n2. ... \n3. ...", "الأدوات": "..."}}
        }}
        """
        try:
            res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            content = res.choices[0].message.content.replace("```json", "").replace("```", "").strip()
            st.session_state.data = json.loads(content)
        except Exception as e:
            st.error(f"خطأ في المعالجة: {e}")

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
                # استخدام replace لجعل الخطوات تظهر بشكل منفصل (عمودي) داخل المربع الأخضر
                with c2: 
                    formatted_steps = act.get('الخطوات', '').replace('. ', '.<br>')
                    st.markdown(f"<div class='box box-steps'><b>📋 الخطوات:</b><br>{formatted_steps}</div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='box box-tools'><b>🛠 الأدوات:</b><br>{act.get('الأدوات', '')}</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓</div>", unsafe_allow_html=True)
