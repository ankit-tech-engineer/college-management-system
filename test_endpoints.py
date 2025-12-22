from fastapi import FastAPI
from modules.auth.passwordModel import ForgotPasswordModel, ResetPasswordModel, ChangePasswordModel

app = FastAPI()

@app.post("/test-forgot")
async def test_forgot(data: ForgotPasswordModel):
    return {"message": "forgot password test"}

@app.post("/test-reset")
async def test_reset(data: ResetPasswordModel):
    return {"message": "reset password test"}

@app.post("/test-change")
async def test_change(data: ChangePasswordModel):
    return {"message": "change password test"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)