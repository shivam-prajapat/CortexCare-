import os
import logging
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from backend.tools import query_medgemma, call_emergency, get_verified_contact_for_user

# ---------- Tools ----------
@tool
def ask_mental_health_specialist(query: str) -> str:
    """Ask the AI mental health specialist for empathetic support."""
    return query_medgemma(query)

@tool
def find_nearby_therapist_by_location(location: str) -> str:
    """Provide a short list of nearby therapists based on a location string."""
    return f"Nearby therapists for {location}: Dr. Ayush Triwedi, Dr. James Patel, MindCare Counseling Center"

# ---------- LLM ----------
llm = ChatOllama(model="llama3.1:8b", temperature=0.7)
SYSTEM_PROMPT = "You are Cortax, an empathetic mental health support assistant."

# ---------- Emergency ----------
def detect_emergency_intent(text: str) -> bool:
    keywords = ["suicide","kill myself","end my life","self harm","hurt myself","want to die","can't go on","help me now","i will kill myself","i want to die"]
    return any(k in text.lower() for k in keywords)

LOG_FILE = os.getenv("EMERGENCY_LOG_FILE", "emergency_audit.log")
logging.basicConfig(level=logging.INFO, filename=LOG_FILE, format='%(asctime)s %(levelname)s %(message)s')
def audit_emergency_action(user_input: str, action: str, details: str):
    logging.info("EMERGENCY | action=%s | input=%s | details=%s", action, user_input, details)

def run_agent(user_input: str):
    agent = create_agent(llm, [ask_mental_health_specialist, find_nearby_therapist_by_location])

    if detect_emergency_intent(user_input):
        audit_emergency_action(user_input, "detected", "emergency_keyword_triggered")
        contact = get_verified_contact_for_user("local_test_user")
        if contact:
            call_emergency(contact)
        system_reply = "⚠️ Emergency detected. Support resources have been contacted automatically."
        return {"messages": [("assistant", system_reply)]}

    return agent.invoke({"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]})

# CLI
if __name__ == "__main__":
    while True:
        msg = input("You: ").strip()
        if msg.lower() in ["exit","quit"]: break
        resp = run_agent(msg)
        print("Bot:", resp["messages"][-1][1] if isinstance(resp["messages"][-1], tuple) else resp["messages"][-1])
