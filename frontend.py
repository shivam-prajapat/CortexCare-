import streamlit as st
import requests

# ---------------- CONFIG ----------------
BACKEND_URL = "http://127.0.0.1:8000/ask"
USER_ID = "local_test_user"

st.set_page_config(
    page_title="CortexCare",
    layout="centered"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>

.stApp {
    background-color: #f8fafc;
}

/* Hide Streamlit default UI */
header, footer, #MainMenu {
    visibility: hidden;
}

/* Header */
.app-header {
    position: sticky;
    top: 0;
    background: #ffffff;
    padding: 18px 0;
    border-bottom: 1px solid #e5e7eb;
    z-index: 100;
}

.app-header h1 {
    text-align: center;
    margin: 0;
    font-size: 30px;
    color: #1e293b;
    font-weight: 700;
}

.app-header p {
    text-align: center;
    margin: 4px 0 0 0;
    color: #64748b;
    font-size: 14px;
}

/* Chat bubbles */
.user {
    background: #e0f2fe;
    padding: 14px 16px;
    border-radius: 14px;
    margin: 10px 0;
    text-align: right;
    color: #0f172a;
}

.assistant {
    background: #ffffff;
    padding: 14px 16px;
    border-radius: 14px;
    margin: 10px 0;
    color: #0f172a;
    border: 1px solid #e5e7eb;
}

/* Input */
.stTextInput input {
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #cbd5f5;
    font-size: 16px;
}

/* Button */
.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 12px;
    padding: 12px 18px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="app-header">
    <h1>CortexCare</h1>
    <p>A calm, private space to talk</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- CHAT ----------------
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"<div class='user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUT ----------------
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])

    with col1:
        user_input = st.text_input(
            "",
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )

    with col2:
        send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.chat.append({
            "role": "user",
            "content": user_input
        })

        try:
            r = requests.post(
                BACKEND_URL,
                json={"message": user_input, "user_id": USER_ID},
                timeout=60
            ).json()
            reply = r.get("reply", "I'm here with you.")
        except Exception:
            reply = "I'm having trouble connecting right now."

        st.session_state.chat.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()
