# backend/email_client.py
import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Try to import google libs; if not available or creds not present, use mock
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except Exception:
    GMAIL_AVAILABLE = False

def fetch_emails_mock(limit=10):
    # Simple mock emails
    out = []
    for i in range(limit):
        out.append({
            "message_id": f"mock-{i}",
            "sender": f"user{i}@example.com",
            "subject": f"Mock subject {i}",
            "snippet": "This is a mock email snippet asking for action.",
            "body": "Hi,\nPlease send the report by Friday.\nThanks.",
            "timestamp": "2025-10-29T10:00:00Z"
        })
    return out

def fetch_emails_from_gmail(limit=50):
    """Sketch: Fetch messages from Gmail via REST API. You must implement OAuth flow separately."""
    creds_path = os.getenv("GMAIL_CREDENTIALS_JSON")
    token_path = os.getenv("GMAIL_TOKEN_JSON")
    if not creds_path or not token_path:
        raise RuntimeError("Gmail credentials/token not configured")
    with open(token_path, "r") as f:
        token = json.load(f)
    creds = Credentials.from_authorized_user_info(token)
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=limit).execute()
    messages = results.get("messages", [])
    out = []
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        snippet = msg.get("snippet")
        body = ""
        parts = msg.get("payload", {}).get("parts", [])
        # simple body extraction (extend for real cases)
        if "data" in msg.get("payload", {}).get("body", {}):
            import base64
            body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"].encode("ASCII")).decode("utf-8")
        else:
            for p in parts:
                if p.get("mimeType") == "text/plain":
                    import base64
                    body = base64.urlsafe_b64decode(p["body"]["data"].encode("ASCII")).decode("utf-8")
        out.append({
            "message_id": m["id"],
            "sender": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "snippet": snippet,
            "body": body,
            "timestamp": headers.get("Date")
        })
    return out

def fetch_emails(limit=10):
    # try real gmail if available, else fallback to mock
    try:
        if GMAIL_AVAILABLE and os.getenv("GMAIL_TOKEN_JSON"):
            return fetch_emails_from_gmail(limit)
    except Exception as e:
        print("Gmail fetch failed:", e)
    return fetch_emails_mock(limit)
