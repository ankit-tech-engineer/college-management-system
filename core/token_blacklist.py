from datetime import datetime, timedelta
from config.database import get_db
import jwt
from config.settings import SECRET_KEY, ALGORITHM

class TokenBlacklist:
    @staticmethod
    async def add_token(token: str):
        """Add token to blacklist"""
        try:
            # Decode token to get expiration
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")
            
            db = await get_db()
            collection = db["blacklisted_tokens"]
            
            await collection.insert_one({
                "token": token,
                "blacklisted_at": datetime.utcnow(),
                "expires_at": datetime.fromtimestamp(exp) if exp else datetime.utcnow() + timedelta(hours=1)
            })
            return True
        except:
            return False
    
    @staticmethod
    async def is_blacklisted(token: str) -> bool:
        """Check if token is blacklisted"""
        try:
            db = await get_db()
            collection = db["blacklisted_tokens"]
            
            result = await collection.find_one({"token": token})
            return result is not None
        except:
            return False
    
    @staticmethod
    async def cleanup_expired():
        """Remove expired tokens from blacklist"""
        try:
            db = await get_db()
            collection = db["blacklisted_tokens"]
            
            await collection.delete_many({
                "expires_at": {"$lt": datetime.utcnow()}
            })
        except:
            pass