import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مصمم الأنشطة الذكي", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🧩 مصمم الأنشطة الذكي")
st.subheader("أدخل اسم الدرس واحصل على أنشطة فورية")

lesson_name = st.text_input("اسم الدرس أو الموضوع:")

if st.button("توليد أنشطة إبداعية"):
    if not lesson_name:
        st.warning("يرجى إدخال اسم الدرس أولاً.")
    else:
        with st.spinner("جاري تصميم أنشطة تناسب درسك..."):
            # الـ Prompt العام الذي لا يتقيد بمادة
            prompt = f"""
            بصفتك مصمماً تعليمياً خبيراً، صمم 3 أنشطة تعليمية متنوعة للدرس التالي: '{lesson_name}'.
            الأنشطة يجب أن تكون:
            1. نشاط استكشافي (يحفز الفضول).
            2. نشاط تطبيقي (يعتمد على الممارسة).
            3. نشاط تقييمي إبداعي (بعيداً عن الاختبارات التقليدية).
            
            لكل نشاط، حدد: (الهدف، خطوات التنفيذ، الأدوات المطلوبة).
            اجعل الأنشطة تناسب أي فئة عمرية، وكن مبتكراً جداً.
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            st.markdown("---")
            st.markdown(response.choices[0].message.content)

st.markdown("---")
st.caption("أداة سريعة لإنتاج أنشطة تعليمية دون تعقيدات.")
