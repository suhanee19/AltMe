# backend/main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv
load_dotenv()

from db import emails_col, actions_col
from email_client import fetch_emails
from classifier import classify
from openai_client import generate_draft_reply
from models import EmailItem, DraftRequest, SendRequest

app = FastAPI(title="Context-Aware Digital Twin (Email)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only; lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/sync_emails")
async def sync_emails(limit: int = 10):
    fetched = fetch_emails(limit=limit)
    inserted = []
    for e in fetched:
        cid = e.get("message_id")
        if not cid:
            continue
        # classification
        cls = classify(e)
        doc = {
            "_id": cid,
            "message_id": cid,
            "sender": e.get("sender"),
            "subject": e.get("subject"),
            "snippet": e.get("snippet"),
            "body": e.get("body"),
            "timestamp": e.get("timestamp"),
            "classification": cls,
            "draft": None,
            "sent": False
        }
        # upsert
        await emails_col.update_one({"_id": cid}, {"$set": doc}, upsert=True)
        inserted.append(cid)
    return {"synced": len(inserted), "ids": inserted}

@app.get("/emails", response_model=List[EmailItem])
async def list_emails(limit: int = 50):
    cursor = emails_col.find().sort("timestamp", -1).limit(limit)
    out = []
    async for d in cursor:
        d["sender"] = d.get("sender","")
        out.append(d)
    return out

@app.post("/draft", response_model=dict)
async def create_draft(req: DraftRequest):
    doc = await emails_col.find_one({"_id": req.message_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Message not found")
    draft = generate_draft_reply(doc.get("subject",""), doc.get("body",""), tone=req.tone, extra_instructions=req.extra_instructions)
    await emails_col.update_one({"_id": req.message_id}, {"$set":{"draft":draft}})
    # log action
    await actions_col.insert_one({
        "message_id": req.message_id,
        "action": "draft_generated",
        "draft": draft
    })
    return {"message_id": req.message_id, "draft": draft}

@app.post("/send")
async def send_draft(req: SendRequest):
    # For demo: we won't actually call Gmail send; mark as sent and log action
    await emails_col.update_one({"_id": req.message_id}, {"$set":{"sent": True}})
    await actions_col.insert_one({
        "message_id": req.message_id,
        "action": "sent",
        "draft": req.draft_text
    })
    return {"status":"ok", "message_id": req.message_id}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
