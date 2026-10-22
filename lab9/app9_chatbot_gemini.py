
import streamlit as st
from google import genai
import time

st.title("Simple Chatbot")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Assistant is typing..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    {
                        "role": "user" if msg["role"] == "user" else "model",
                        "parts": [{"text": msg["content"]}]
                    }
                    for msg in st.session_state.messages
                ]
            )

            reply = response.text

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.write(reply)

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

if st.session_state.messages:
    chat_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages
    )

    st.download_button(
        "Download Chat",
        chat_text,
        "chat_history.txt",
        "text/plain"
    )
