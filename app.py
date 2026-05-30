import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مؤرخ المستقبل", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY.")
    st.stop()

st.title("مؤرخ المستقبل (Future Historian)")

tab1, tab2, tab3 = st.tabs(["تصميم الأنشطة الإثرائية", "تحليل النقد البنّاء", "بنك الأسئلة"])

with tab1:
    topic = st.text_input("الموضوع التاريخي:")
    if st.button("توليد الأنشطة الإثرائية"):
        # الـ Prompt المحدث بناءً على المحتوى الأكاديمي الدقيق
        prompt = f"""
        بصفتك خبيراً في التربية التاريخية، صمم أنشطة إثرائية للموضوع '{topic}' بناءً على 'العقول الخمسة للمستقبل' لهوارد غاردنر كما يلي:
        1. العقل المنضبط: ركز على تدريب الطلاب على أدوات المؤرخ (تحليل الوثائق، تقييم الموثوقية، استكشاف الدوافع).
        2. العقل التركيبي: ركز على ربط المفاهيم عبر دمج مصادر متنوعة (نصوص، خرائط، وسائط رقمية) لاكتشاف الروابط الكلية.
        3. العقل المبدع: ركز على 'التخيل التاريخي' وطرح تساؤلات افتراضية (ماذا لو...) لتحويل الدرس لمشكلة مفتوحة.
        4. العقل المحترم: ركز على إدارة النقاشات القائمة على الحوار وتقبل الآخر والتعدد الحضاري.
        5. العقل الأخلاقي: ركز على تأمل الأبعاد الأخلاقية والقيم الإنسانية (العدالة، المسؤولية) وتشكيل الضمير الإنساني.
        
        ممنوع منعاً باتاً ذكر 'الذكاءات المتعددة' أو العقول (اللغوية، الرياضية، الموسيقية). التزم فقط بالتعريفات أعلاه.
        """
        response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        st.markdown(response.choices[0].message.content)

with tab2:
    st.write("أدخل إجابة الطالب لتحليلها تربوياً بناءً على العقول الخمسة:")
    student_ans = st.text_area("إجابة الطالب:")
    if st.button("تحليل النقد البنّاء"):
        feedback_prompt = f"قدم نقداً تربوياً بنّاءً بناءً على نظرية العقول الخمسة لغاردنر لإجابة الطالب: {student_ans} حول {topic}."
        response = client.chat.completions.create(messages=[{"role": "user", "content": feedback_prompt}], model="llama-3.3-70b-versatile")
        st.success(response.choices[0].message.content)

with tab3:
    if st.button("توليد أسئلة التفكير التاريخي"):
        q_prompt = f"صمم 5 أسئلة تاريخية غير مألوفة لموضوع '{topic}' تحفز التفكير النقدي بعيداً عن الاستظهار."
        response = client.chat.completions.create(messages=[{"role": "user", "content": q_prompt}], model="llama-3.3-70b-versatile")
        st.warning(response.choices[0].message.content)

st.write("---")
st.write("المطور: عدي عبد الرحمن | مرجع: العقول الخمسة للمستقبل - هوارد غاردنر")
