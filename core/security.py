from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from config.settings import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Hash password, truncating to 72 characters if needed (bcrypt limit)."""
    if len(password) > 72:
        password = password[:72]  # Truncate string (safe for ASCII; for full UTF-8, use bytes below)
    # Alternative for precise UTF-8 byte truncation:
    # password_bytes = password.encode('utf-8')[:72]
    # password = password_bytes.decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)