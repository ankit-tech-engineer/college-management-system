from datetime import datetime, timedelta
from fastapi import HTTPException, status
from core.security import hash_password, verify_password, create_access_token
from config.database import get_db
from modules.auth.authModel import LoginModel, RegisterModel, CompleteProfileModel
from core.auto_increment import get_next_sequence
from core.response import create_response
from core.token_blacklist import TokenBlacklist
from core.email_service import EmailService
from core.otp_service import OTPService
from modules.roles.roleService import RoleService
from bson import ObjectId
import re

class AuthService:
    def __init__(self):
        self.email_service = EmailService()
        self.otp_service = OTPService()
        self.role_service = RoleService()
    
    async def get_collection(self):
        db = await get_db()
        return db["users"]

    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        if len(password.encode('utf-8')) > 72:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        return True

    def _validate_phone(self, phone: str) -> bool:
        """Validate Indian phone number format"""
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        indian_patterns = [
            r'^\+91[6-9]\d{9}$',
            r'^91[6-9]\d{9}$',
            r'^[6-9]\d{9}$'
        ]
        return any(re.match(pattern, clean_phone) for pattern in indian_patterns)

    async def register(self, user_data: RegisterModel):
        try:
            collection = await self.get_collection()
            existing_email = await collection.find_one({"email": user_data.email})
            if existing_email:
                return create_response(
                    success=False,
                    code=400,
                    message="Email already registered",
                    data=None
                )
            
            existing_phone = await collection.find_one({"phone_number": user_data.phone_number})
            if existing_phone:
                return create_response(
                    success=False,
                    code=400,
                    message="Phone number already registered",
                    data=None
                )

            if not self._validate_password(user_data.password):
                return create_response(
                    success=False,
                    code=400,
                    message="Password must be 8+ characters with uppercase, lowercase, and number",
                    data=None
                )

            if not self._validate_phone(user_data.phone_number):
                return create_response(
                    success=False,
                    code=400,
                    message="Invalid phone number format",
                    data=None
                )

            user_doc = {
                "id": await get_next_sequence("users"),
                "full_name": user_data.full_name,
                "email": user_data.email,
                "phone_number": user_data.phone_number,
                "password": hash_password(user_data.password),
                "role": "student",
                "profile_completed": False,
                "application_status": "pending",
                "is_active": True,
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            result = await collection.insert_one(user_doc)
            
            otp = await self.otp_service.create_otp(user_data.email)
            email_sent = False
            if otp:
                email_sent = await self.email_service.send_welcome_otp_email(
                    email=user_data.email,
                    full_name=user_data.full_name,
                    user_id=str(result.inserted_id),
                    otp=otp
                )
            
            return create_response(
                message="User registered successfully. Please verify your email with the OTP sent.",
                data={
                    "user_id": str(result.inserted_id),
                    "email": user_data.email,
                    "email_sent": email_sent,
                    "verification_required": True
                }
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def complete_profile(self, user_id: str, profile_data: CompleteProfileModel):
        try:
            collection = await self.get_collection()
            user = await collection.find_one({"_id": ObjectId(user_id), "is_deleted": False})
            
            if not user:
                return create_response(
                    success=False,
                    code=404,
                    message="User not found",
                    data=None
                )
            
            update_doc = {"updated_at": datetime.utcnow()}
            
            if profile_data.personalDetails:
                personal_details = user.get("personalDetails", {})
                pd = profile_data.personalDetails
                if pd.full_name:
                    personal_details["full_name"] = pd.full_name
                if pd.father_name:
                    personal_details["father_name"] = pd.father_name
                if pd.dob:
                    personal_details["dob"] = pd.dob
                if pd.gender:
                    personal_details["gender"] = pd.gender
                if pd.address:
                    personal_details["address"] = pd.address
                if pd.city:
                    personal_details["city"] = pd.city
                if pd.state:
                    personal_details["state"] = pd.state
                if pd.country:
                    personal_details["country"] = pd.country
                if pd.pincode:
                    personal_details["pincode"] = pd.pincode
                if pd.phone_number:
                    personal_details["phone_number"] = pd.phone_number
                if pd.alt_number is not None:
                    personal_details["alt_number"] = pd.alt_number
                update_doc["personalDetails"] = personal_details
            
            if profile_data.academicDetails:
                academic_details = user.get("academicDetails", {})
                if profile_data.academicDetails.tenth:
                    academic_details["tenth"] = profile_data.academicDetails.tenth.dict()
                if profile_data.academicDetails.twelfth:
                    academic_details["twelfth"] = profile_data.academicDetails.twelfth.dict()
                if profile_data.academicDetails.previousCollege:
                    academic_details["previousCollege"] = profile_data.academicDetails.previousCollege.dict()
                update_doc["academicDetails"] = academic_details
            
            if profile_data.courseSelection:
                course_selection = user.get("courseSelection", {})
                if profile_data.courseSelection.program:
                    course_selection["program"] = profile_data.courseSelection.program
                if profile_data.courseSelection.course:
                    course_selection["course"] = profile_data.courseSelection.course
                update_doc["courseSelection"] = course_selection
            
            if profile_data.photo:
                update_doc["photo"] = profile_data.photo
            
            if profile_data.id_proof:
                update_doc["id_proof"] = profile_data.id_proof
            
            updated_user = await collection.find_one({"_id": ObjectId(user_id)})
            if updated_user:
                has_photo = profile_data.photo or updated_user.get("photo")
                has_id_proof = profile_data.id_proof or updated_user.get("id_proof")
                if has_photo and has_id_proof:
                    update_doc["profile_completed"] = True
                    update_doc["application_status"] = "applied"
                    
                    if user.get("role") == "student":
                        db = await get_db()
                        students_collection = db["students"]
                        existing_student = await students_collection.find_one({"user_id": user["id"]})
                        if not existing_student:
                            student_doc = {
                                "id": await get_next_sequence("students"),
                                "user_id": user["id"],
                                "full_name": user["full_name"],
                                "email": user["email"],
                                "phone_number": user["phone_number"],
                                "personalDetails": update_doc.get("personalDetails", updated_user.get("personalDetails", {})),
                                "academicDetails": update_doc.get("academicDetails", updated_user.get("academicDetails", {})),
                                "courseSelection": update_doc.get("courseSelection", updated_user.get("courseSelection", {})),
                                "photo": update_doc.get("photo", updated_user.get("photo", {})),
                                "id_proof": update_doc.get("id_proof", updated_user.get("id_proof", {})),
                                "application_status": "applied",
                                "is_deleted": False,
                                "created_at": datetime.utcnow(),
                                "updated_at": datetime.utcnow()
                            }
                            await students_collection.insert_one(student_doc)
            
            await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_doc}
            )
            
            return create_response(
                message="Profile updated successfully",
                data={"profile_completed": update_doc.get("profile_completed", False)}
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )

    async def login(self, login_data: LoginModel):
        try:
            collection = await self.get_collection()
            user = await collection.find_one({
                "email": login_data.email,
                "is_deleted": False
            })

            if not user or not verify_password(login_data.password, user["password"]):
                return create_response(
                    success=False,
                    code=401,
                    message="Invalid email or password",
                    data=None
                )
            
            is_verified = await self.otp_service.is_email_verified(login_data.email)
            if not is_verified:
                return create_response(
                    success=False,
                    code=403,
                    message="Please verify your email address before logging in",
                    data=None
                )

            if not user.get("is_active", True):
                return create_response(
                    success=False,
                    code=401,
                    message="Account is deactivated",
                    data=None
                )

            access_token_expires = timedelta(minutes=60)
            access_token = create_access_token(
                data={"sub": str(user["_id"]), "email": user["email"], "role": user.get("role")},
                expires_delta=access_token_expires
            )

            return create_response(
                message="Login successful",
                data={
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": str(user["_id"]),
                        "full_name": user["full_name"],
                        "email": user["email"],
                        "phone_number": user["phone_number"],
                        "role": user.get("role", "student"),
                        "profile_completed": user.get("profile_completed", False),
                        "application_status": user.get("application_status", "pending"),
                        "is_active": user.get("is_active", True),
                        "created_at": user["created_at"]
                    }
                }
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def logout(self, token: str):
        """Logout user by blacklisting token"""
        try:
            success = await TokenBlacklist.add_token(token)
            if success:
                return create_response(
                    message="Logged out successfully",
                    data=None
                )
            else:
                return create_response(
                    success=False,
                    code=400,
                    message="Failed to logout",
                    data=None
                )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def forgot_password(self, email: str):
        """Send password reset OTP to user email"""
        try:
            collection = await self.get_collection()
            user = await collection.find_one({"email": email, "is_deleted": False})
            
            if not user:
                return create_response(
                    success=False,
                    code=404,
                    message="User not found",
                    data=None
                )
            
            otp = await self.otp_service.create_otp(email)
            if not otp:
                return create_response(
                    success=False,
                    code=500,
                    message="Failed to generate OTP",
                    data=None
                )
            
            email_sent = await self.email_service.send_forgot_password_email(
                email=email,
                full_name=user.get("full_name", "User"),
                otp=otp
            )
            
            return create_response(
                message="Password reset OTP sent to your email",
                data={"email_sent": email_sent}
            )
            
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def reset_password(self, email: str, otp: str, new_password: str):
        """Reset password using OTP"""
        try:
            otp_result = await self.otp_service.verify_otp(email, otp)
            if not otp_result["success"]:
                return create_response(
                    success=False,
                    code=400,
                    message=otp_result["message"],
                    data=None
                )
            
            if not self._validate_password(new_password):
                return create_response(
                    success=False,
                    code=400,
                    message="Password must be 8+ characters with uppercase, lowercase, and number",
                    data=None
                )
            
            collection = await self.get_collection()
            user = await collection.find_one({"email": email, "is_deleted": False})
            
            if not user:
                return create_response(
                    success=False,
                    code=404,
                    message="User not found",
                    data=None
                )
            
            hashed_password = hash_password(new_password)
            await collection.update_one(
                {"_id": user["_id"]},
                {"$set": {
                    "password": hashed_password,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            await self.email_service.send_password_reset_success_email(
                email=email,
                full_name=user.get("full_name", "User")
            )
            
            return create_response(
                message="Password reset successfully",
                data=None
            )
            
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def change_password(self, user_id: str, current_password: str, new_password: str):
        """Change password for authenticated user"""
        try:
            collection = await self.get_collection()
            user = await collection.find_one({"_id": ObjectId(user_id), "is_deleted": False})
            
            if not user:
                return create_response(
                    success=False,
                    code=404,
                    message="User not found",
                    data=None
                )
            
            if not verify_password(current_password, user["password"]):
                return create_response(
                    success=False,
                    code=400,
                    message="Current password is incorrect",
                    data=None
                )
            
            if not self._validate_password(new_password):
                return create_response(
                    success=False,
                    code=400,
                    message="Password must be 8+ characters with uppercase, lowercase, and number",
                    data=None
                )
            
            hashed_password = hash_password(new_password)
            await collection.update_one(
                {"_id": user["_id"]},
                {"$set": {
                    "password": hashed_password,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            return create_response(
                message="Password changed successfully",
                data=None
            )
            
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )