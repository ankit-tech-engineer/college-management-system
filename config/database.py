from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_URI, DB_NAME

client = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    print("Connected to MongoDB successfully")

async def get_db():
    return db