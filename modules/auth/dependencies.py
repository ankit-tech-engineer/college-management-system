from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
import jwt
from jwt.exceptions import InvalidTokenError
from config.settings import SECRET_KEY, ALGORITHM
from config.database import get_db
from bson import ObjectId
from core.token_blacklist import TokenBlacklist
from core.response import create_response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

class AuthException(Exception):
    def __init__(self, message: str, code: int = 401):
        self.message = message
        self.code = code

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = AuthException("Not authenticated", 401)
    
    try:
        # Check if token is blacklisted
        if await TokenBlacklist.is_blacklisted(token):
            raise credentials_exception
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        db = await get_db()
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user or user.get("is_deleted"):
            raise credentials_exception
        return user
    except AuthException:
        raise credentials_exception
    except (InvalidTokenError, Exception):
        raise credentials_exception

def require_role(role: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != role:
            raise AuthException("Access forbidden: insufficient permissions", 403)
        return current_user
    return role_checker