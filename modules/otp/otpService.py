from core.otp_service import OTPService
from core.response import create_response
from core.email_service import EmailService
from modules.otp.otpModel import OTPVerifyModel, OTPRegenerateModel
from config.database import get_db

class OTPServiceHandler:
    def __init__(self):
        self.otp_service = OTPService()
        self.email_service = EmailService()
    
    async def verify_otp(self, otp_data: OTPVerifyModel):
        """Verify OTP for user"""
        try:
            result = await self.otp_service.verify_otp(
                user_identifier=otp_data.email,
                otp=otp_data.otp
            )
            
            if result["success"]:
                # Get user details and send success email
                try:
                    db = await get_db()
                    user = await db["users"].find_one({"email": otp_data.email})
                    if user:
                        await self.email_service.send_verification_success_email(
                            email=otp_data.email,
                            full_name=user.get("full_name", "User")
                        )
                except:
                    pass  # Don't fail verification if email sending fails
                
                return create_response(
                    message=result["message"],
                    data={"verified": True}
                )
            else:
                return create_response(
                    success=False,
                    code=400,
                    message=result["message"],
                    data=None
                )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def regenerate_otp(self, regenerate_data: OTPRegenerateModel):
        """Regenerate OTP for user"""
        try:
            # Check if user exists
            db = await get_db()
            user = await db["users"].find_one({"email": regenerate_data.email})
            if not user:
                return create_response(
                    success=False,
                    code=404,
                    message="User not found",
                    data=None
                )
            
            # Generate new OTP
            otp = await self.otp_service.create_otp(regenerate_data.email)
            if not otp:
                return create_response(
                    success=False,
                    code=500,
                    message="Failed to generate OTP",
                    data=None
                )
            
            # Send new OTP email
            email_sent = await self.email_service.send_welcome_otp_email(
                email=regenerate_data.email,
                full_name=user.get("full_name", "User"),
                user_id=str(user["_id"]),
                otp=otp
            )
            
            return create_response(
                message="New OTP sent to your email",
                data={"email_sent": email_sent}
            )
            
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )