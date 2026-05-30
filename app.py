import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مولد إثراء التاريخ", layout="wide")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("تأكد من إضافة GROQ_API_KEY في إعدادات Secrets.")
    st.stop()

# التنسيق
st.markdown("""
<style>
.stApp {background-color: #0e1117; color: white;}
.card {padding: 20px; border-radius: 15px; background-color: #1e2530; border: 1px solid #333; margin: 10px; text-align: center; color: white; min-height: 200px;}
.footer {text-align: center; margin-top: 50px; color: #888;}
</style>
""", unsafe_allow_html=True)

st.title("مولد إثراء التاريخ")
st.subheader("ستوديو تصميم الذكاء الاصطناعي - عقول غاردنر الخمسة")

col1, col2 = st.columns(2)
topic = col1.text_input("أدخل الموضوع التاريخي:")
age_group = col2.selectbox("اختر المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

if st.button("توليد النشاط"):
    if not topic:
        st.warning("يرجى إدخال موضوع!")
    else:
        with st.spinner("جاري التوليد باستخدام أحدث نموذج..."):
            try:
                prompt = f"صمم 5 أنشطة تاريخية عن {topic} للمرحلة {age_group} بناءً على عقول غاردنر الخمسة. أجب في 5 نقاط مختصرة."
                
                # استخدام النموذج الجديد المدعوم
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                
                res_text = response.choices[0].message.content
                activities = res_text.split('\n')
                
                cols = st.columns(5)
                minds = ["المنضبط", "المركب", "المبدع", "المحترم", "الأخلاقي"]
                for i, col in enumerate(cols):
                    with col:
                        st.markdown(f"<div class='card'><b>{minds[i]}</b><br><br>{activities[i] if i<len(activities) else '...'}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"خطأ في الاتصال بالنموذج: {e}")
