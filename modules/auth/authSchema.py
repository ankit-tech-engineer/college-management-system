from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone_number: str
    role: str = "student"
    is_active: bool = True
    created_at: datetime

class RegisterResponse(BaseModel):
    message: str
    user_id: str
    email: EmailStr

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserResponse