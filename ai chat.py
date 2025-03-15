from openai import OpenAI
import streamlit as st
from streamlit_lottie import st_lottie
import json

# تحميل ملف Lottie
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# تهيئة عميل OpenAI
client = OpenAI(api_key="sk-mnopqrstijkl5678mnopqrstijkl5678mnopqrst")
# عرض الأنيميشن
lottie_animation = load_lottie_file("animation.json")
st_lottie(lottie_animation, speed=1, height=300, key="chatbot")

# عنوان التطبيق
st.title("🤖 AI Chatbot - Powered by HB LORD")

# واجهة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض محادثات سابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم إلى المحادثة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # إرسال رسالة المستخدم إلى OpenAI والحصول على الرد
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # إضافة رد البوت إلى المحادثة
    st.session_state.messages.append({"role": "assistant", "content": reply})
