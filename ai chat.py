import torch
from transformers import GPTJForCausalLM, AutoTokenizer
import streamlit as st

# تحميل النموذج (GPT-J 6B)
model_name = "EleutherAI/gpt-j-6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = GPTJForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to("cuda")

# عنوان التطبيق
st.title("🤖 AI Chatbot - Powered by GPT-J")

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

    # إرسال رسالة المستخدم إلى النموذج والحصول على الرد
    with st.chat_message("assistant"):
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_length=100, temperature=0.7)
        reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.markdown(reply)

    # إضافة رد البوت إلى المحادثة
    st.session_state.messages.append({"role": "assistant", "content": reply})
