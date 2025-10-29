# backend/openai_client.py
import os
import openai
from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    print("Warning: OPENAI_API_KEY not set. Draft generation will fail.")
else:
    openai.api_key = OPENAI_KEY

def generate_draft_reply(subject: str, body: str, tone: str="professional", extra_instructions: str=""):
    """
    Uses OpenAI Completion or Chat API to produce a short draft reply.
    """
    if not OPENAI_KEY:
        return "OpenAI API key not configured. (mock reply) Thank you — I will review and get back to you."
    prompt = (
        f"You are an assistant writing a short reply in a {tone} tone.\n"
        f"Email subject: {subject}\n"
        f"Email body: {body}\n"
        f"Additional instructions: {extra_instructions}\n\n"
        "Write a concise reply (1-3 short paragraphs) acknowledging and describing next steps where relevant:"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # or "gpt-4o" / "gpt-4" check your available models
        messages=[
            {"role":"system","content":"You are a helpful assistant drafting concise professional email replies."},
            {"role":"user","content":prompt}
        ],
        max_tokens=300,
        temperature=0.2,
    )
    text = resp["choices"][0]["message"]["content"].strip()
    return text
