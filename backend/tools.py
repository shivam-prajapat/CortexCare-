import os
from typing import Optional
import ollama
from twilio.rest import Client

# ---------------- MedGemma AI ----------------
def query_medgemma(prompt: str) -> str:
    system_prompt = """
You are Cortax, a warm, experienced, and ethical emotional support guide.
Respond empathetically and calmly.
Never diagnose or prescribe; always encourage professional help when needed.
"""
    try:
        response = ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={"num_predict": 350, "temperature": 0.7, "top_p": 0.9}
        )
        return response["message"]["content"].strip()
    except Exception:
        return "I'm having a little trouble responding right now. Please try again in a moment."

# ---------------- Emergency Call ----------------
def call_emergency(emergency_contact: str) -> bool:
    """Place a call using Twilio. Returns True if successful."""
    try:
        TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

        if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER):
            print("❌ Twilio credentials missing in environment")
            return False

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            to=emergency_contact,
            from_=TWILIO_FROM_NUMBER,
            url="https://demo.twilio.com/docs/voice.xml"
        )
        return True if getattr(call, "sid", None) else False
    except Exception as e:
        print("call_emergency error:", e)
        return False

# ---------------- Verified Contact ----------------
def get_verified_contact_for_user(user_id: str) -> Optional[str]:
    env_contact = os.getenv("EMERGENCY_CONTACT")
    if env_contact:
        return env_contact

    fallback = {"local_test_user": "+918273333639"}  # replace with real number
    return fallback.get(user_id)
