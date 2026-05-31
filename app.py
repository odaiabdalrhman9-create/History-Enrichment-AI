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

st.markdown("<h1 style='text-align:center'>⚡ مصمم الأنشطة الإثرائية الذكي (نسخة الخبير التربوي)</h1>", unsafe_allow_html=True)

# المدخلات
lesson_name = st.text_input("💡 اسم الدرس:", placeholder="مثال: تاريخ الدولة الزنكية")
strategy = st.selectbox("🎯 اختر استراتيجية التعلم:", 
                        ["التعلم القائم على المشكلات", "لعب الأدوار", "التفكير الناقد", "الخرائط الذهنية", "المحاكاة التاريخية"])
grade_level = st.select_slider("🎓 المرحلة:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if 'data' not in st.session_state: st.session_state.data = None

# Prompt مُطور بـ "الفلسفة التربوية"
def get_prompt(lesson, grade, strategy):
    return f"""
    أنت خبير تربوي متخصص في تصميم المناهج. صمم 3 أنشطة إثرائية لدرس '{lesson}' للمرحلة '{grade}' باستخدام استراتيجية '{strategy}'.
    
    قواعد تعليمية صارمة:
    1. ابتعد تماماً عن الأنشطة البحثية التقليدية (مثل: 'ابحث عن معلومات واكتب تقريراً').
    2. صمم أنشطة تعتمد على مستويات التفكير العليا (التحليل، التقييم، الإبداع).
    3. 'الخطوات' يجب أن تكون إجرائية وتفاعلية (مثال: 'حلل'، 'اقترح'، 'قارن'، 'صمم سيناريو').
    4. 'تقويم' يجب أن يصف كيف سنقيس أداء الطالب أو فهمه العميق.
    5. المخرج JSON فقط. لا أسطر جديدة داخل النصوص.
    
    الهيكل:
    {{
        "نشاط1": {{"اسم": "...", "الهدف": "...", "الخطوات": ["خ1", "خ2"], "الأدوات": "...", "تقويم": "..."}},
        ...
    }}
    """

if st.button("🚀 توليد أنشطة إثرائية إبداعية"):
    with st.spinner("جاري تصميم الأنشطة وفق المعايير التربوية..."):
        try:
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": get_prompt(lesson_name, grade_level, strategy)}], 
                model="llama-3.3-70b-versatile"
            )
            raw = res.choices[0].message.content.replace("```json", "").replace("```", "").strip()
            
            try:
                st.session_state.data = json.loads(raw)
            except:
                st.session_state.data = ast.literal_eval(raw)
            
        except Exception as e:
            st.error(f"حدث خطأ تربوي في صياغة الأنشطة: {e}")

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
                st.markdown(f"<div class='box box-goal'><b>🎯 الهدف الإثرائي:</b><br>{act.get('الهدف')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='box box-tools'><b>🛠 الأدوات:</b><br>{act.get('الأدوات')}</div>", unsafe_allow_html=True)
            with c2:
                steps_html = "".join([f"<li>{s}</li>" for s in act.get('الخطوات', [])])
                st.markdown(f"<div class='box box-steps'><b>📋 خطوات الاستراتيجية ({strategy}):</b><br><ol>{steps_html}</ol></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='box box-eval'><b>✅ التقويم البنائي:</b><br>{act.get('تقويم')}</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; color:white; margin-top:50px;'>تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓</div>", unsafe_allow_html=True)
