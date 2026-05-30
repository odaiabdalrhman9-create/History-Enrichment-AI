import streamlit as st
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# إعداد الصفحة
st.set_page_config(page_title="مؤرخ المستقبل", layout="wide")

# إعداد الـ Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في إعدادات Secrets.")
    st.stop()

# التنسيق البصري
st.markdown("""
    <style>
    .stApp {background-color: #f8f9fa;}
    .card {padding: 25px; border-radius: 12px; background-color: #ffffff; border-left: 6px solid #0056b3; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px;}
    .title-box {text-align: center; color: #0056b3; margin-bottom: 40px;}
    .footer {text-align: center; margin-top: 60px; color: #6c757d; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-box'><h1>مؤرخ المستقبل (Future Historian)</h1><p>بيئة التعلم التاريخي القائمة على العقول الخمسة</p></div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["تصميم الأنشطة الإثرائية", "تحليل النقد البنّاء", "بنك الأسئلة غير المألوفة"])

with tab1:
    topic = st.text_input("الموضوع التاريخي:")
    age_group = st.selectbox("المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"], key="age1")
    
    if st.button("توليد الأنشطة الإثرائية"):
        prompt = f"""
        بصفتك خبيراً في التربية التاريخية، صمم أنشطة إثرائية للمرحلة {age_group} حول موضوع '{topic}' 
        بناءً حصراً على 'العقول الخمسة للمستقبل' لهوارد غاردنر:
        1. العقل المنضبط: ركز على تدريب الطلاب على أدوات المؤرخ (تحليل الوثائق، تقييم الموثوقية، استكشاف السياقات).
        2. العقل التركيبي: ركز على ربط المفاهيم والوقائع عبر دمج مصادر متنوعة (نصوص، خرائط، وسائط رقمية).
        3. العقل المبدع: ركز على 'التخيل التاريخي' وطرح تساؤلات افتراضية (ماذا لو...) كبديل للفهم التقليدي.
        4. العقل المحترم: ركز على إدارة النقاشات القائمة على الحوار، تقبل الرأي الآخر، والتعدد الحضاري.
        5. العقل الأخلاقي: ركز على تأمل الأبعاد القيمية (العدالة، المسؤولية) وتشكيل الضمير الإنساني.
        
        تحذير: ممنوع منعاً باتاً ذكر 'الذكاءات المتعددة' أو العقول (اللغوية، الرياضية، الموسيقية). التزم فقط بالتعريفات أعلاه.
        """
        response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        st.markdown(f"<div class='card'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)

with tab2:
    st.write("أدخل إجابة الطالب لتحليلها تربوياً بناءً على العقول الخمسة:")
    student_ans = st.text_area("إجابة الطالب:")
    
    if st.button("تحليل النقد البنّاء"):
        feedback_prompt = f"""
        بصفتك خبيراً تربوياً، قدم تحليلاً ونقداً بناءً لإجابة الطالب التالية حول موضوع '{topic}' 
        بناءً حصراً على 'العقول الخمسة للمستقبل' لهوارد غاردنر.
        
        حلل الإجابة بناءً على هذه المعايير:
        1. العقل المنضبط: هل أظهر الطالب فهماً منهجياً وأدوات تحليل تاريخية؟
        2. العقل التركيبي: هل ربط الطالب المفاهيم ضمن إطار شامل؟
        3. العقل المبدع: هل قدم الطالب رؤية جديدة أو تساؤلاً ابتكارياً؟
        4. العقل المحترم: هل أظهر انفتاحاً وتعدداً في وجهات النظر؟
        5. العقل الأخلاقي: هل لمس الطالب أبعاداً قيمية؟
        
        ممنوع منعاً باتاً استخدام أي مصطلحات مثل (نقد لغوي، نقد رياضي، نقد منطقي). 
        اجعل النقد موجهاً لتطوير التفكير التاريخي لدى الطالب.
        إجابة الطالب هي: {student_ans}
        """
        response = client.chat.completions.create(messages=[{"role": "user", "content": feedback_prompt}], model="llama-3.3-70b-versatile")
        st.success(response.choices[0].message.content)

with tab3:
    if st.button("توليد أسئلة التفكير التاريخي غير المألوفة"):
        q_prompt = f"صمم 5 أسئلة تاريخية غير مألوفة وغير تقليدية حول '{topic}' لتحفيز التفكير النقدي والإبداعي، بعيداً عن الاستظهار."
        response = client.chat.completions.create(messages=[{"role": "user", "content": q_prompt}], model="llama-3.3-70b-versatile")
        st.warning(response.choices[0].message.content)

st.markdown("<div class='footer'>المطور: عدي عبد الرحمن | نظرية العقول الخمسة للمستقبل - هوارد غاردنر</div>", unsafe_allow_html=True)
