from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from backend.tools import query_medgemma, call_emergency, get_verified_contact_for_user

app = FastAPI(title="CortexCare API")

class Query(BaseModel):
    message: str
    user_id: Optional[str] = "local_user"

EMERGENCY_KEYWORDS = [
    "i want to die", "kill myself", "end my life",
    "suicide", "self harm", "can't go on"
]

def detect_emergency(text: str) -> bool:
    text = text.lower()
    return any(k in text for k in EMERGENCY_KEYWORDS)

@app.post("/ask")
async def ask(query: Query):
    text = query.message.strip()

    if detect_emergency(text):
        contact = get_verified_contact_for_user(query.user_id)
        call_status = False

        if contact:
            call_status = call_emergency(contact)

        safe_prompt = f"""
User is in emotional crisis.
Acknowledge pain.
Encourage staying alive.
Do NOT say emergency was contacted.
"""
        reply = query_medgemma(safe_prompt)

        return {
            "reply": reply,
            "emergency_triggered": True,
            "call_success": call_status
        }

    reply = query_medgemma(text)
    return {"reply": reply, "emergency_triggered": False}
