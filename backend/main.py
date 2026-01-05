from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os

from backend.tools import query_medgemma, call_emergency, get_verified_contact_for_user

app = FastAPI(title="CortexCare API")

# ---------------- Models ----------------
class Query(BaseModel):
    message: str
    user_id: Optional[str] = "local_test_user"

# ---------------- Emergency Detector ----------------
def detect_emergency_intent(text: str) -> bool:
    emergency_keywords = [
        "suicide", "kill myself", "end my life",
        "i want to die", "i will kill myself",
        "hurt myself", "self harm", "can't go on",
        "i am done with life", "help me now"
    ]
    return any(k in text.lower() for k in emergency_keywords)

# ---------------- Endpoints ----------------
@app.post("/ask")
async def ask(query: Query):
    user_message = query.message.strip()

    # 🚨 Emergency detected
    if detect_emergency_intent(user_message):
        contact = get_verified_contact_for_user(query.user_id)
        if contact:
            success = call_emergency(contact)
            status_msg = "Emergency call placed successfully." if success else "Emergency call failed."
        else:
            status_msg = "No verified contact found. Please contact local emergency services immediately."

        # LLM reply for crisis
        crisis_prompt = f"""
User said: "{user_message}"
Respond empathetically as a trained emotional support guide.
Acknowledge distress, encourage staying alive,
and inform that emergency help has been contacted automatically.
Do not ask for permission.
"""
        reply = query_medgemma(crisis_prompt)

        return {
            "reply": reply,
            "emergency_triggered": True,
            "call_status": status_msg
        }

    # ---------- Normal conversation ----------
    reply = query_medgemma(user_message)
    return {"reply": reply, "emergency_triggered": False}
