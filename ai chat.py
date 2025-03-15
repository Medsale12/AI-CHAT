import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# تهيئة التطبيق
def تهيئة_التطبيق():
    st.set_page_config(page_title="دردشة فريدة", page_icon="💬")
    st.title("دردشة ذكية مع Hugging Face")
    st.write("مرحبًا! أنا هنا لأجيب على أسئلتك.")

# تحميل النموذج والـ Tokenizer
def تحميل_النموذج():
    النموذج = AutoModelForCausalLM.from_pretrained("facebook/blenderbot-400M-distill")
    الـtokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
    return النموذج, الـtokenizer

# إنشاء واجهة المستخدم
def إنشاء_واجهة_المستخدم(النموذج, الـtokenizer):
    if "المحادثات" not in st.session_state:
        st.session_state.المحادثات = []

    with st.form("دردشة"):
        المدخلات = st.text_area("اكتب رسالتك هنا:")
        if st.form_submit_button("إرسال"):
            if المدخلات.strip() != "":
                with st.spinner("جارٍ التفكير..."):
                    # تحضير المدخلات للنموذج
                    مدخلات_مشفرة = الـtokenizer.encode(المدخلات + الـtokenizer.eos_token, return_tensors="pt")
                    ناتج_مشفر = النموذج.generate(مدخلات_مشفرة, max_length=1000, pad_token_id=الـtokenizer.eos_token_id)
                    الرد = الـtokenizer.decode(ناتج_مشفر[:, مدخلات_مشفرة.shape[-1]:][0], skip_special_tokens=True)

                    # حفظ المحادثة
                    st.session_state.المحادثات.append(("أنت", المدخلات))
                    st.session_state.المحادثات.append(("الذكاء الاصطناعي", الرد))

    # عرض المحادثات
    for المرسل, الرسالة in st.session_state.المحادثات:
        if المرسل == "أنت":
            st.markdown(f"**أنت:** {الرسالة}")
        else:
            st.markdown(f"**الذكاء الاصطناعي:** {الرسالة}")

# تشغيل التطبيق
def تشغيل_التطبيق():
    تهيئة_التطبيق()
    النموذج, الـtokenizer = تحميل_النموذج()
    إنشاء_واجهة_المستخدم(النموذج, الـtokenizer)

if __name__ == "__main__":
    تشغيل_التطبيق()
