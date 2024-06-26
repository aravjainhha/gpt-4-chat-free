import streamlit as st
from openai import OpenAI

st.title("GPT-4 Chat (free)")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "We appreciate your engagement! Please note, this free version is designed to process a maximum of 5 interactions. Thank you for your understanding."
    )

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Maximum allowed messages
max_messages = (
    10  # Counting both user and assistant messages, so 5 iterations of conversation
)

if len(st.session_state.messages) >= max_messages:
    st.info(
        """Notice: The maximum message limit for this demo version has been reached."""
    )

else:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
