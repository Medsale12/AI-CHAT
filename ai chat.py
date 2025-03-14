import openai
import streamlit as st
from streamlit_lottie import st_lottie
import json

# تحميل ملف Lottie (JSON)
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# تعيين مفتاح API الخاص بـ OpenAI
openai.api_key = "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"

# عنوان التطبيق مع أيقونة
st.title("🤖 AI Chatbot - Powered by Mohamed Salem El Batal")

# عرض أنيميشن Lottie
lottie_animation = load_lottie_file("animation.json")  # قم بتحميل ملف JSON الخاص بالأنيميشن
st_lottie(lottie_animation, speed=1, height=200, key="initial")

# تهيئة محادثة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض محادثات سابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم إلى المحادثة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # إرسال رسالة المستخدم إلى OpenAI والحصول على الرد
    with st.chat_message("assistant", avatar="🤖"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # يمكنك استخدام "gpt-4" إذا كان متاحًا
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        reply = st.write_stream(response["choices"][0]["message"]["content"])

    # إضافة رد البوت إلى المحادثة
    st.session_state.messages.append({"role": "assistant", "content": reply})