import streamlit as st
from groq import Groq

# 1. إعداد الصفحة وتنسيق الهوية البصرية (Professional Educational UI)
st.set_page_config(page_title="مؤرخ المستقبل - Future Historian", layout="wide")

# إعداد الـ Client للذكاء الاصطناعي
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("خطأ: يرجى ضبط GROQ_API_KEY في إعدادات Secrets.")
    st.stop()

# 2. تصميم الواجهة باستخدام CSS (ألوان تربوية: أزرق ملكي، أبيض، رمادي هادئ)
st.markdown("""
    <style>
    .stApp {background-color: #fcfcfc;}
    .main-title {text-align: center; color: #1e3a8a; font-size: 45px; font-weight: bold; margin-bottom: 5px;}
    .sub-title {text-align: center; color: #555; font-size: 20px; margin-bottom: 40px;}
    .stTabs [data-baseweb="tab-list"] {gap: 24px; justify-content: center;}
    .stTabs [data-baseweb="tab"] {background-color: #f1f5f9; border-radius: 8px; padding: 10px 20px; color: #1e3a8a;}
    .stTabs [aria-selected="true"] {background-color: #1e3a8a !important; color: white !important;}
    .result-card {padding: 30px; border-radius: 15px; background-color: #ffffff; border-right: 8px solid #1e3a8a; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-top: 20px;}
    .footer {text-align: center; margin-top: 80px; padding: 20px; color: #64748b; border-top: 1px solid #e2e8f0; font-family: 'Arial';}
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (العنوان واسم التطبيق)
st.markdown("<div class='main-title'>مؤرخ المستقبل (Future Historian)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>بيئة هندسة التعلم التاريخي القائمة على العقول الخمسة للمستقبل</div>", unsafe_allow_html=True)

# 4. الحقول الأساسية (تظهر في جميع التبويبات لضمان استمرارية الموضوع)
col1, col2 = st.columns([2, 1])
with col1:
    topic = st.text_input("📍 أدخل الموضوع التاريخي (مثال: الدولة المملوكية):", placeholder="اكتب الموضوع هنا...")
with col2:
    age_group = st.selectbox("🎓 المرحلة الدراسية:", ["ابتدائية", "إعدادية", "ثانوية"])

# 5. تبويبات التطبيق الرئيسية
tab1, tab2, tab3 = st.tabs(["📋 تصميم الأنشطة الإثرائية", "🔍 تحليل النقد البنّاء", "💡 بنك الأسئلة غير المألوفة"])

# --- التبويب الأول: تصميم الأنشطة ---
with tab1:
    st.write("استخدم هذا القسم لتصميم مهام تعليمية تعمق التفكير التاريخي.")
    if st.button("توليد الأنشطة الإثرائية"):
        if not topic:
            st.warning("يرجى إدخال الموضوع أولاً!")
        else:
            with st.spinner("جاري تصميم الأنشطة بناءً على المرجعية الأكاديمية..."):
                prompt = f"""
                بصفتك خبيراً في التربية التاريخية، صمم أنشطة إثرائية للمرحلة {age_group} حول موضوع '{topic}' 
                بناءً حصراً على 'العقول الخمسة للمستقبل' لهوارد غاردنر (2007) والتعريفات التالية:
                
                1. العقل المنضبط: تدريب الطلاب على أدوات المؤرخ (تحليل الوثائق، تقييم الموثوقية، استكشاف السياقات والدوافع).
                2. العقل التركيبي: ربط المفاهيم والوقائع عبر دمج مصادر متنوعة (نصوص، خرائط، وسائط رقمية) لاكتشاف الروابط الكلية.
                3. العقل المبدع: تفعيل 'التخيل التاريخي' وطرح تساؤلات افتراضية (ماذا لو...) لتحويل الدرس لمشكلة مفتوحة.
                4. العقل المحترم: إدارة نقاشات قائمة على الحوار وتقبل الرأي الآخر وتوظيف المواقف التي تظهر التعدد الحضاري.
                5. العقل الأخلاقي: تأمل الأبعاد الأخلاقية للأحداث (العدالة، المسؤولية) وتشكيل الضمير الإنساني الواعي بالحاضر.
                
                تحذير صارم: لا تستخدم الذكاءات المتعددة (لغوي، منطقي، موسيقي.. إلخ). 
                المخرجات يجب أن تكون: (الهدف التربوي، النشاط الإثرائي، أداة التقييم) لكل عقل.
                """
                try:
                    response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                    st.markdown(f"<div class='result-card'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"حدث خطأ في الاتصال: {e}")

# --- التبويب الثاني: تحليل النقد البنّاء ---
with tab2:
    st.write("حلل إجابات الطلاب وقدم تغذية راجعة تربوية تعزز عقول المستقبل.")
    student_ans = st.text_area("ألصق إجابة الطالب هنا:")
    
    if st.button("تحليل النقد البنّاء"):
        if not topic or not student_ans:
            st.warning("يرجى التأكد من إدخال الموضوع وإجابة الطالب.")
        else:
            with st.spinner("جاري تشريح الإجابة تربوياً..."):
                feedback_prompt = f"""
                بصفتك خبيراً تربوياً، قدم تحليلاً ونقداً بناءً لإجابة الطالب التالية حول موضوع '{topic}'.
                يجب أن يكون النقد قائماً حصراً على 'العقول الخمسة للمستقبل' (المنضبط، التركيبي، المبدع، المحترم، الأخلاقي).
                
                المطلوب:
                - تقييم الإجابة من منظور كل عقل من العقول الخمسة (بناءً على مفاهيم التفكير التاريخي).
                - تقديم نصائح عملية للطالب لتطوير تفكيره التاريخي في هذا الموضوع تحديداً.
                
                تحذير: ممنوع منعاً باتاً استخدام مصطلحات النقد (اللغوي، المنطقي، الرياضي، الموسيقي، الحركي). 
                اجعل التحليل أكاديمياً ومرتبطاً بالموضوع التاريخي المذكور.
                إجابة الطالب هي: {student_ans}
                """
                try:
                    response = client.chat.completions.create(messages=[{"role": "user", "content": feedback_prompt}], model="llama-3.3-70b-versatile")
                    st.markdown(f"<div class='result-card'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

# --- التبويب الثالث: بنك الأسئلة ---
with tab3:
    st.write("ولد أسئلة تحفز التفكير النقدي العميق بعيداً عن الحفظ والاستظهار.")
    if st.button("توليد أسئلة التفكير التاريخي"):
        if not topic:
            st.warning("يرجى إدخال الموضوع أولاً!")
        else:
            with st.spinner(f"جاري صياغة أسئلة غير مألوفة حول {topic}..."):
                q_prompt = f"""
                صمم 5 أسئلة تاريخية 'غير مألوفة' ومحفزة للتفكير النقدي حول موضوع '{topic}' حصراً.
                يجب أن تخدم الأسئلة تنمية العقول الخمسة:
                - أسئلة افتراضية (ماذا لو..).
                - أسئلة نقدية للمصادر والدوافع.
                - أسئلة ربط حضاري كلي.
                - أسئلة حول الأبعاد الأخلاقية والقيمية للحدث.
                
                تحذير: لا تولد أسئلة عامة عن التاريخ. يجب أن تكون الأسئلة مرتبطة ارتباطاً وثيقاً بـ '{topic}'.
                """
                try:
                    response = client.chat.completions.create(messages=[{"role": "user", "content": q_prompt}], model="llama-3.3-70b-versatile")
                    st.markdown(f"<div class='result-card'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

# الفوتر (التوقيع والمرجع)
st.markdown(f"""
    <div class='footer'>
        تطوير: <b>عدي عبد الرحمن</b> | 
        المرجع الأكاديمي: نظرية العقول الخمسة للمستقبل (هوارد غاردنر) <br>
        <i>تم التصميم لتعزيز مهارات التفكير التاريخي والاستقصاء المنهجي</i>
    </div>
""", unsafe_allow_html=True)
