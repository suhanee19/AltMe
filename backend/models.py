# backend/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

class EmailItem(BaseModel):
    message_id: str
    sender: EmailStr
    subject: str
    snippet: Optional[str]
    body: Optional[str]
    timestamp: Optional[str]
    labels: Optional[List[str]] = []
    classification: Optional[str] = None
    draft: Optional[str] = None
    sent: Optional[bool] = False

class DraftRequest(BaseModel):
    message_id: str
    tone: Optional[str] = "professional"
    extra_instructions: Optional[str] = ""

class SendRequest(BaseModel):
    message_id: str
    draft_text: str
