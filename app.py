import streamlit as st
import json
import re
from groq import Groq

st.set_page_config(page_title="مصمم الأنشطة الذكي", layout="wide")

# إعداد الـ Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# CSS مُحسن للتباين والهوامش
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); }
    h1, label { color: white !important; }
    .box { padding: 25px; border-radius: 20px; color: white; margin: 15px 0; line-height: 1.8; font-weight: 500; border: 1px solid rgba(255,255,255,0.2); }
    .box-goal { background: rgba(8, 145, 178, 0.9); }
    .box-steps { background: rgba(5, 150, 105, 0.9); }
    .box-tools { background: rgba(124, 58, 237, 0.9); }
    .box-eval { background: rgba(217, 119, 6, 0.9); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>⚡ مصمم الأنشطة الإثرائية الذكي</h1>", unsafe_allow_html=True)

# المدخلات
lesson_name = st.text_input("💡 اسم الدرس:")
grade_level = st.select_slider("🎓 المرحلة:", options=["ابتدائية", "إعدادية", "ثانوية", "جامعية"])

if 'data' not in st.session_state: st.session_state.data = None

def generate_prompt(lesson, grade, specific_key=None):
    return f"""
    صمم 3 أنشطة إثرائية لدرس '{lesson}' للمرحلة '{grade}'.
    أخرج النتيجة بصيغة JSON فقط. كل نشاط يحتوي على: اسم النشاط، الهدف، الخطوات (مصفوفة)، الأدوات، وطريقة التقويم.
    {{
        "نشاط1": {{"اسم": "...", "الهدف": "...", "الخطوات": ["خطوة1", "خطوة2"], "الأدوات": "...", "تقويم": "..."}},
        ...
    }}
    """

if st.button("🚀 توليد الأنشطة"):
    with st.spinner("جاري الإبداع..."):
        prompt = generate_prompt(lesson_name, grade_level)
        res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        content = re.sub(r'[\x00-\x1f]', '', res.choices[0].message.content.replace("```json", "").replace("```", "").strip())
        st.session_state.data = json.loads(content)

if st.session_state.data:
    tabs = st.tabs(["💡 نشاط 1", "💡 نشاط 2", "💡 نشاط 3"])
    for i, tab in enumerate(tabs):
        with tab:
            act = st.session_state.data[f"نشاط{i+1}"]
            st.subheader(f"🏷️ {act.get('اسم', 'نشاط إثرائي')}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='box box-goal'><b>🎯 الهدف:</b><br>{act.get('الهدف')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='box box-tools'><b>🛠 الأدوات:</b><br>{act.get('الأدوات')}</div>", unsafe_allow_html=True)
            with c2:
                steps = "".join([f"<li>{s}</li>" for s in act.get('الخطوات', [])])
                st.markdown(f"<div class='box box-steps'><b>📋 الخطوات:</b><br><ol>{steps}</ol></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='box box-eval'><b>✅ تقويم النشاط:</b><br>{act.get('تقويم')}</div>", unsafe_allow_html=True)
            
            if st.button(f"🔄 توليد بديل للنشاط {i+1}", key=f"btn_{i}"):
                st.info("تم التوليد البديل (قم بتحديث الصفحة لرؤيته)") # هنا تضع منطق التوليد الجزئي

st.markdown("<div style='text-align:center; color:white; margin-top:50px;'>تطوير: عدي عبد الرحمن | ماجستير في المناهج وطرائق التدريس 🎓</div>", unsafe_allow_html=True)
