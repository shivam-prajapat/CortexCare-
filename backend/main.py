from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from backend.tools import query_medgemma, call_emergency, get_verified_contact_for_user

app = FastAPI(title="CortexCare API")

# ---------- Models ----------
class Query(BaseModel):
    message: str
    user_id: Optional[str] = "local_user"

# ---------- Emergency Detection ----------
EMERGENCY_KEYWORDS = [
    "i want to die",
    "want to die",
    "kill myself",
    "end my life",
    "suicide",
    "self harm",
    "hurt myself",
    "can't go on",
    "dont want to live",
    "i am done"
]

def detect_emergency(text: str) -> bool:
    text = text.lower().strip()
    return any(k in text for k in EMERGENCY_KEYWORDS)

# ---------- Endpoint ----------
@app.post("/ask")
async def ask(query: Query):
    user_text = query.message.strip()

    # 🚨 Emergency flow
    if detect_emergency(user_text):
        contact = get_verified_contact_for_user(query.user_id)
        call_success = False

        if contact:
            call_success = call_emergency(contact)

        crisis_prompt = f"""
User said: "{user_text}"

Respond as a calm, empathetic emotional support guide.
Acknowledge the pain and seriousness of their feelings.
Encourage them to stay alive and seek help.
Do NOT mention phone calls, emergency systems, or automation.
Do NOT give instructions for self-harm.
"""
        reply = query_medgemma(crisis_prompt)

        return {
            "reply": reply,
            "emergency_triggered": True,
            "call_success": call_success
        }

    # 🟢 Normal conversation
    reply = query_medgemma(user_text)
    return {
        "reply": reply,
        "emergency_triggered": False
    }
