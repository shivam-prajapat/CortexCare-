import streamlit as st

st.set_page_config(page_title="AI Mental Health Therapist", layout ="wide")

st.title("CortexCare - AI Mental Health Therapist")

#Initialize chat history in session state

if "chat_history" not in  st.session_state:
    st.session_state.chat_history=[]

#chat  input

user_input=st.chat_input("Hey buddy, what's on your mind today?")
if user_input:
    st.session_state.chat_history.append({"role":"user","content":user_input})

    fixed_dummy_response="I'm here for you . Its ok to feel that way.Would you like to talk more about it"
    st.session_state.chat_history.append({"role":"assistant","content":fixed_dummy_response})

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        

