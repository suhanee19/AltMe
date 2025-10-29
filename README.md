# Context-Aware Digital Twin — Email Prototype

## Overview
Prototype that:
- Fetches emails (mock or Gmail),
- Classifies them (rule-based + ML),
- Generates draft replies using OpenAI,
- Stores everything in MongoDB,
- Simple frontend to view, approve, and "send" drafts.

## Prerequisites
- Python 3.10+
- Node/npm or static file server (optional)
- MongoDB Atlas or local MongoDB
- OpenAI API key
- (Optional) Google Gmail API credentials & token

## Setup

1. Clone
```bash
git clone <repo>
cd digital-twin-email/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
