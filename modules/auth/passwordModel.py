from pydantic import BaseModel

class ForgotPasswordModel(BaseModel):
    email: str

class ResetPasswordModel(BaseModel):
    email: str
    otp: str
    new_password: str

class ChangePasswordModel(BaseModel):
    current_password: str
    new_password: str