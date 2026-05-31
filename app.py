import streamlit as st
import json
import re
import ast
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مصمم الأنشطة الإثرائي الذكي", layout="wide", page_icon="⚡")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في إعدادات التطبيق.")
    st.stop()

# التصميم (CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    h1, label, h3 { color: #ffffff !important; }
    .box { padding: 25px; border-radius: 20px; color: #ffffff; margin: 15px 0; line-height: 1.8; font-weight: 500; border: 1px solid rgba(255,255,255,0.2); }
    .box-goal { background: rgba(8, 145, 178, 0.9); } 
    .box-steps { background: rgba(5, 150, 105, 0.9); } 
    .box-tools { background: rgba(124, 58, 237, 0.9); } 
    .box-eval { background: rgba(217, 119, 6, 0.9); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>⚡ مصمم الأنشطة الإثرائية الذكي</h1>", unsafe_allow_html=True)

lesson_name = st.text_input("💡 اسم الدرس:", placeholder="مثال: تاريخ الدولة المملوكية")
grade_level = st.select_slider("🎓 المرحلة:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if 'data' not in st.session_state: st.session_state.data = None

# Prompt مُحكم جداً لمنع انهيار الـ JSON
def get_prompt(lesson, grade):
    return f"""
    صمم 3 أنشطة إثرائية لدرس '{lesson}' للمرحلة '{grade}'.
    أخرج النتيجة بصيغة JSON فقط.
    قواعد صارمة: 
    1. لا تضف أي أسطر جديدة (\n) داخل نصوص القيم.
    2. تأكد من إغلاق علامات التنصيص والفواصل بشكل صحيح.
    3. الهيكل:
    {{
        "نشاط1": {{"اسم": "...", "الهدف": "...", "الخطوات": ["خ1", "خ2"], "الأدوات": "...", "تقويم": "..."}},
        "نشاط2": {{"اسم": "...", "الهدف": "...", "الخطوات": ["خ1", "خ2"], "الأدوات": "...", "تقويم": "..."}},
        "نشاط3": {{"اسم": "...", "الهدف": "...", "الخطوات": ["خ1", "خ2"], "الأدوات": "...", "تقويم": "..."}}
    }}
    """

if st.button("🚀 توليد الأنشطة الإثرائية"):
    with st.spinner("جاري صياغة الأنشطة..."):
        try:
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": get_prompt(lesson_name, grade_level)}], 
                model="llama-3.3-70b-versatile"
            )
            raw = res.choices[0].message.content.replace("```json", "").replace("```", "").strip()
            
            # محاولة التحويل لـ JSON، إذا فشل نستخدم ast للتعامل مع نصوص أقل صرامة
            try:
                st.session_state.data = json.loads(raw)
            except:
                # محاولة بديلة إذا كان التنسيق يحتوي على أخطاء بسيطة
                st.session_state.data = ast.literal_eval(raw)
            
        except Exception as e:
            st.error(f"حدث خطأ: تأكد من اسم الدرس. الخطأ: {e}")

# عرض النتائج
if st.session_state.data:
    keys = list(st.session_state.data.keys())
    tabs = st.tabs([f"💡 {st.session_state.data[k].get('اسم', 'نشاط')}" for k in keys])
    
    for i, tab in enumerate(tabs):
        with tab:
            act = st.session_state.data[keys[i]]
            st.subheader(f"🏷️ {act.get('اسم')}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='box box-goal'><b>🎯 الهدف:</b><br>{act.get('الهدف')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='box box-tools'><b>🛠 الأدوات:</b><br>{act.get('الأدوات')}</div>", unsafe_allow_html=True)
            with c2:
                steps_html = "".join([f"<li>{s}</li>" for s in act.get('الخطوات', [])])
                st.markdown(f"<div class='box box-steps'><b>📋 الخطوات:</b><br><ol>{steps_html}</ol></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='box box-eval'><b>✅ تقويم النشاط:</b><br>{act.get('تقويم')}</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; color:white; margin-top:50px;'>تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓</div>", unsafe_allow_html=True)
