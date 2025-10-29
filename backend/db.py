# backend/db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
if not MONGO_URI:
    raise RuntimeError("MONGODB_URI not set in environment")

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()

# collections
emails_col = db["emails"]
users_col = db["users"]
actions_col = db["actions"]
