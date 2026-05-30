import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="مولد إثراء التاريخ", layout="wide")

# محاولة الاتصال بـ Groq باستخدام الـ Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("خطأ في إعدادات Secrets: تأكد من إضافة GROQ_API_KEY")
    st.stop()

# التنسيق
st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color: white;}
    .card {
        padding: 20px;
        border-radius: 15px
