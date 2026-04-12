import streamlit as st
import os
from rag_engine import build_rag_chain, ask

st.set_page_config(
    page_title="Chat with Shruti's AI",
    page_icon="👩‍💻",
    layout="centered"
)

st.markdown("""
<style>
    .main-header { text-align: center; padding: 1rem 0; }
    .stChatMessage { padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("👩‍💻 Shruti Verma — AI Persona")
st.caption("Ask me about my experience, projects, skills, or book a call!")

# load API keys from streamlit secrets
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]


@st.cache_resource
def load_chain():
    return build_rag_chain(data_dir="data")


try:
    chain = load_chain()
except Exception as e:
    st.error(f"Error loading RAG chain: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! I'm Shruti's AI persona. You can ask me about my work experience, projects, skills, or anything from my resume and GitHub. What would you like to know? 😊"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("thinking..."):
            response = ask(chain, prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.markdown("### 📅 Book a Call")
    st.markdown("Want to chat with the real Shruti?")
    st.link_button("Book on Cal.com", "https://cal.com/shruti.verma", use_container_width=True)
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("- [GitHub](https://github.com/crazyshrut)")
    st.markdown("- [Email](mailto:shrutiverma032003@gmail.com)")
    st.markdown("---")
    st.caption("This AI is RAG-grounded on my real resume and GitHub repos. It doesn't make stuff up.")
