from pydantic import BaseModel

class OTPVerifyModel(BaseModel):
    email: str
    otp: str

class OTPRegenerateModel(BaseModel):
    email: str