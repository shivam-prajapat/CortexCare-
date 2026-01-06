import os
from typing import Optional
import ollama
from twilio.rest import Client

# ---------------- MedGemma AI ----------------
def query_medgemma(prompt: str) -> str:
    system_prompt = """
You are Cortax, a calm, ethical emotional support guide.
Never claim to contact emergency services.
If user is in distress, encourage professional help.
"""
    try:
        response = ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={"num_predict": 300, "temperature": 0.7}
        )
        return response["message"]["content"].strip()
    except Exception:
        return "I'm having trouble responding right now. Please try again."

# ---------------- Emergency Call ----------------
def call_emergency(emergency_contact: str) -> bool:
    try:
        sid = os.environ.get("TWILIO_ACCOUNT_SID")
        token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_number = os.environ.get("TWILIO_FROM_NUMBER")

        if not all([sid, token, from_number]):
            print("❌ Twilio ENV missing")
            return False

        client = Client(sid, token)
        call = client.calls.create(
            to=emergency_contact,
            from_=from_number,
            url="https://demo.twilio.com/docs/voice.xml"
        )

        print("📞 Call SID:", call.sid)
        return True

    except Exception as e:
        print("❌ call_emergency error:", e)
        return False

# ---------------- Verified Contact ----------------
def get_verified_contact_for_user(user_id: str) -> Optional[str]:
    return os.environ.get("EMERGENCY_CONTACT")
