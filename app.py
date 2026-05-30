import streamlit as st
from groq import Groq

# 1. إعدادات الهوية البصرية والجمالية (RPG & Professional UI)
st.set_page_config(page_title="مؤرخ المستقبل | Future Historian", layout="wide", page_icon="📜")

# إعداد العميل
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("يرجى ضبط GROQ_API_KEY في إعدادات Secrets.")
    st.stop()

# تصميم الواجهة باستخدام CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Cairo', sans-serif;
        background-color: #f0f2f6;
    }
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #10b981 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .quest-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 10px solid #10b981;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .badge-box {
        display: inline-block;
        padding: 10px 20px;
        background: #fef3c7;
        border: 2px solid #f59e0b;
        border-radius: 50px;
        color: #92400e;
        font-weight: bold;
        margin-top: 10px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# 2. الهيكل الرئيسي للتطبيق
st.markdown("""
    <div class='main-header'>
        <h1>📜 مؤرخ المستقبل: رحلة العقول الخمسة</h1>
        <p>قم بتحويل التاريخ إلى مهمة استكشافية عالمية</p>
    </div>
""", unsafe_allow_html=True)

# إدارة حالة التطبيق (للحفاظ على التقدم والشارات)
if 'badges' not in st.session_state:
    st.session_state['badges'] = []

# 3. المدخلات الأساسية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2682/2682065.png", width=100)
    st.title("إعدادات الرحلة")
    topic = st.text_input("📍 الموضوع التاريخي:", placeholder="مثلاً: الدولة المملوكية")
    age_group = st.selectbox("👥 الفئة المستهدفة:", ["ابتدائية", "إعدادية", "ثانوية"])
    quest_level = st.select_slider("⚔️ مستوى الصعوبة:", options=["مبتدئ", "خبير", "مؤرخ عظيم"])
    
    st.info(f"المستوى الحالي: {quest_level}")
    if st.session_state['badges']:
        st.write("🏆 أوسمتك المحققة:")
        for b in set(st.session_state['badges']):
            st.markdown(f"✅ {b}")

# 4. التبويبات الهجينة (معلم + طالب)
tab1, tab2, tab3, tab4 = st.tabs(["🎮 لوحة المهمات (Quests)", "🔬 مختبر التحليل", "💡 مخزن الأسئلة", "📜 سجل الإنجاز"])

# --- التبويب الأول: لوحة المهمات (نمط الطالب والمعلم) ---
with tab1:
    st.subheader("قم بتوليد " + quest_level + " لموضوع " + topic)
    if st.button("إطلاق المهمة التاريخية 🚀"):
        if not topic:
            st.warning("أدخل موضوعاً لتبدأ الرحلة!")
        else:
            with st.spinner("جاري بناء عالم المهمة..."):
                prompt = f"""
                بصفتك مصمم ألعاب تعليمية وخبير تاريخ، صمم 'مهمة تاريخية' (Quest) لموضوع '{topic}' للمرحلة {age_group} بمستوى '{quest_level}'.
                يجب أن تشرك المهمة الطالب في الأدوار التالية بناءً على العقول الخمسة لغاردنر:
                1. مهمة العقل المنضبط: 'المحقق التاريخي' (تحليل وثيقة أو مصدر).
                2. مهمة العقل التركيبي: 'مهندس الروابط' (ربط الحدث بمتغيرات أخرى).
                3. مهمة العقل المبدع: 'المتخيل التاريخي' (سيناريو ماذا لو).
                4. مهمة العقل المحترم: 'دبلوماسي الحضارات' (حوار وتقبل الآخر).
                5. مهمة العقل الأخلاقي: 'حارس القيم' (اتخاذ قرار أخلاقي تجاه الحدث).
                
                اجعل الأسلوب مشوقاً (RPG Style) واذكر في نهاية كل مهمة اسم 'الوسام' الذي سيحصل عليه الطالب.
                تحذير: لا تذكر الذكاءات المتعددة. التزم بالعقول الخمسة للمستقبل فقط.
                """
                res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
                result = res.choices[0].message.content
                st.markdown(f"<div class='quest-card'>{result}</div>", unsafe_allow_html=True)
                st.session_state['last_quest'] = result

# --- التبويب الثاني: مختبر التحليل (نمط المعلم) ---
with tab2:
    st.subheader("تحليل إجابة الطالب (نقد بناء)")
    student_input = st.text_area("ألصق إجابة الطالب هنا ليتم تشريحها بناءً على العقول الخمسة:")
    if st.button("تشغيل التحليل المخبري 🔍"):
        if not student_input:
            st.error("لا توجد إجابة لتحليلها!")
        else:
            with st.spinner("جاري التحليل الأكاديمي..."):
                feedback_prompt = f"""
                حلل إجابة الطالب التالية حول موضوع '{topic}' بناءً على معايير العقول الخمسة للتفكير التاريخي:
                - العقل المنضبط (المنهجية).
                - العقل التركيبي (الربط).
                - العقل المبدع (الابتكار).
                - العقل المحترم (الانفتاح).
                - العقل الأخلاقي (الضمير).
                
                ممنوع استخدام مصطلحات الذكاءات المتعددة (لغوي، رياضي.. إلخ). 
                وجه الطالب كيف يطور تفكيره التاريخي في المرة القادمة.
                إجابة الطالب: {student_input}
                """
                res = client.chat.completions.create(messages=[{"role": "user", "content": feedback_prompt}], model="llama-3.3-70b-versatile")
                st.info(res.choices[0].message.content)
                # محاكاة منح وسام بناءً على جودة الإجابة
                st.session_state['badges'].append("وسام المحلل الناقد")

# --- التبويب الثالث: مخزن الأسئلة ---
with tab3:
    st.subheader("أسئلة التفكير غير المألوف")
    if st.button("توليد أسئلة التحدي 💡"):
        with st.spinner("جاري استخراج أسئلة من خارج الصندوق..."):
            q_prompt = f"صمم 5 أسئلة تاريخية غير مألوفة وعميقة حول موضوع '{topic}' تهدف لاستفزاز التفكير النقدي والإبداعي لدى الطلاب."
            res = client.chat.completions.create(messages=[{"role": "user", "content": q_prompt}], model="llama-3.3-70b-versatile")
            st.warning(res.choices[0].message.content)

# --- التبويب الرابع: سجل الإنجاز ---
with tab4:
    st.subheader("📜 سجل رحلتك التاريخية")
    if not st.session_state['badges']:
        st.write("لم تبدأ رحلتك بعد.. أكمل المهمات للحصول على الأوسمة!")
    else:
        cols = st.columns(3)
        for i, badge in enumerate(set(st.session_state['badges'])):
            cols[i % 3].markdown(f"<div class='badge-box'>🏆 {badge}</div>", unsafe_allow_html=True)
    
    if 'last_quest' in st.session_state:
        with st.expander("عرض آخر مهمة قمت بتوليدها"):
            st.write(st.session_state['last_quest'])

# الفوتر
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px; padding: 20px; color: #64748b;'>
        تطوير: <b>عُدي عبد الرحمن</b> | تطبيق 'مؤرخ المستقبل' V2.0 <br>
        قائم على نظرية العقول الخمسة للمستقبل - هوارد غاردنر
    </div>
""", unsafe_allow_html=True)
