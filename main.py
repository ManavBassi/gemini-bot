import numpy as np
import pandas as pd
import time
import streamlit as st
import google.generativeai as gpt

API_KEY=st.secrets["GEMINI_KEY"]

def fetch_gemini_response(user_query):
    # use session model to  generate response
    response =st.session_state.chat_session.model.generate_content(user_query)
    print(f"Gemini's Response : {response}")
    return response.parts[0].text

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role
    
gpt.configure(api_key=API_KEY)
model=gpt.GenerativeModel('gemini-1.5-flash')
        
# initialize chat session in streamlit if not allready present
if "chat_session" not in st.session_state:
    st.session_state.chat_session=model.start_chat(history=[])

# display the chatbot title on th page
st.title("chat with Gemini-pro")

# display the chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg['role'])):
        st.markdown(msg['content'])

prompt=st.chat_input('say something')
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    gemini_response= fetch_gemini_response(prompt)
    
    st.session_state.chat_session.history.append({"role": "user", "content": prompt})
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response})

    with st.chat_message("assistant"):
        st.write_stream(stream_data(gemini_response))