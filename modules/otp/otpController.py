from fastapi import APIRouter, Depends
from modules.otp.otpModel import OTPVerifyModel, OTPRegenerateModel
from modules.otp.otpService import OTPServiceHandler
from modules.permissions.permissionService import PermissionService

router = APIRouter()
otp_service = OTPServiceHandler()
permission_service = PermissionService()

@router.post("/verify")
async def verify_otp(otp_data: OTPVerifyModel):
    """
    Verify OTP for email verification (Public)
    """
    result = await otp_service.verify_otp(otp_data)
    return result

@router.post("/regenerate")
async def regenerate_otp(regenerate_data: OTPRegenerateModel):
    """
    Regenerate OTP for email verification (Public)
    """
    result = await otp_service.regenerate_otp(regenerate_data)
    return result