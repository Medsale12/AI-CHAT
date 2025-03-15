import requests
import streamlit as st

# عنوان التطبيق
st.title("🤖 AI Chatbot - Powered by Hugging Face")

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

    # إرسال رسالة المستخدم إلى Hugging Face API
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    headers = {"Authorization": "Bearer your_hugging_face_api_key_here"}
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)
    reply = response.json()[0]["generated_text"]

    # عرض رد البوت
    with st.chat_message("assistant"):
        st.markdown(reply)

    # إضافة رد البوت إلى المحادثة
    st.session_state.messages.append({"role": "assistant", "content": reply})
