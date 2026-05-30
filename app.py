import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مؤرخ المستقبل", layout="wide")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في إعدادات Secrets.")
    st.stop()

st.title("مؤرخ المستقبل (Future Historian)")
st.subheader("تصميم بيئة التعلم التاريخي القائمة على العقول الخمسة")

# تبويبات التطبيق
tab1, tab2, tab3 = st.tabs(["تصميم المهام", "تحليل النقد البنّاء", "بنك الأسئلة غير المألوفة"])

with tab1:
    col1, col2 = st.columns(2)
    topic = col1.text_input("الموضوع التاريخي:")
    time_limit = col2.text_input("الوقت المخصص (مثال: 45 دقيقة):")
    
    if st.button("توليد الأنشطة الإثرائية"):
        prompt = f"""
        صمم أنشطة تعليمية لموضوع '{topic}' بزمن {time_limit} بناءً على عقول غاردنر الخمسة.
        لكل عقل: 1. الهدف التربوي، 2. النشاط الإثرائي، 3. معايير التقييم.
        """
        response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        st.info(response.choices[0].message.content)

with tab2:
    st.write("أدخل إجابة الطالب لتقديم تغذية راجعة من منظور العقول الخمسة:")
    student_ans = st.text_area("إجابة الطالب:")
    if st.button("تحليل النقد البنّاء"):
        feedback_prompt = f"قدم نقداً تربوياً بنّاءً لإجابة الطالب التالية حول {topic} من منظور العقول الخمسة لغاردنر: {student_ans}"
        response = client.chat.completions.create(messages=[{"role": "user", "content": feedback_prompt}], model="llama-3.3-70b-versatile")
        st.success(response.choices[0].message.content)

with tab3:
    if st.button("توليد أسئلة التفكير غير المألوف"):
        question_prompt = f"صمم 5 أسئلة تاريخية غير مألوفة وغير تقليدية حول {topic} لتحفيز التفكير الإبداعي والتحليلي."
        response = client.chat.completions.create(messages=[{"role": "user", "content": question_prompt}], model="llama-3.3-70b-versatile")
        st.warning(response.choices[0].message.content)

st.markdown("---")
st.write("المطور: عدي عبد الرحمن")
