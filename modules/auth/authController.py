from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from modules.auth.authModel import LoginModel, RegisterModel, CompleteProfileModel
from modules.auth.passwordModel import ForgotPasswordModel, ResetPasswordModel, ChangePasswordModel
from modules.auth.authSchema import LoginResponse, RegisterResponse, TokenResponse
from modules.auth.authService import AuthService
from modules.auth.dependencies import get_current_user, oauth2_scheme
from modules.permissions.permissionService import PermissionService
from core.response import create_response

router = APIRouter()
auth_service = AuthService()
permission_service = PermissionService()

@router.post("/register")
async def register(user_data: RegisterModel, response: Response):
    """
    Register a new student with basic information
    """
    result = await auth_service.register(user_data)
    response.status_code = result.get("code", 200)
    return result

@router.post("/complete-profile")
async def complete_profile(profile_data: CompleteProfileModel, response: Response, current_user: dict = Depends(get_current_user)):
    """
    Complete student profile with personal, academic, course, and document details
    """
    result = await auth_service.complete_profile(str(current_user["_id"]), profile_data)
    response.status_code = result.get("code", 200)
    return result

@router.post("/login")
async def login(login_data: LoginModel, response: Response):
    """
    Authenticate user and return access token
    """
    result = await auth_service.login(login_data)
    response.status_code = result.get("code", 200)
    return result

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login endpoint
    """
    login_data = LoginModel(email=form_data.username, password=form_data.password)
    result = await auth_service.login(login_data)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Return standard OAuth2 token response (not wrapped)
    return {
        "access_token": result["data"]["access_token"],
        "token_type": "bearer"
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(permission_service.require_permission("auth", "read"))):
    """
    Get current authenticated user information
    """
    user_data = {
        "id": current_user["id"],
        "full_name": current_user["full_name"],
        "email": current_user["email"],
        "phone_number": current_user["phone_number"],
        "role": current_user.get("role", "student"),
        "profile_completed": current_user.get("profile_completed", False),
        "application_status": current_user.get("application_status", "pending"),
        "is_active": current_user.get("is_active", True),
        "created_at": current_user.get("created_at")
    }
    
    if current_user.get("profile_completed"):
        user_data["personalDetails"] = current_user.get("personalDetails", {})
        user_data["academicDetails"] = current_user.get("academicDetails", {})
        user_data["courseSelection"] = current_user.get("courseSelection", {})
        user_data["photo"] = current_user.get("photo", {})
        user_data["id_proof"] = current_user.get("id_proof", {})
    
    return create_response(
        message="User information retrieved successfully",
        data=user_data
    )

@router.post("/logout")
async def logout(response: Response, token: str = Depends(oauth2_scheme)):
    """
    Logout user by blacklisting token
    """
    result = await auth_service.logout(token)
    response.status_code = result.get("code", 200)
    return result

@router.post("/forgot-password")
async def forgot_password(forgot_data: ForgotPasswordModel, response: Response):
    """
    Send password reset OTP to email
    
    - **email**: User's email address
    """
    result = await auth_service.forgot_password(forgot_data.email)
    response.status_code = result.get("code", 200)
    return result

@router.post("/reset-password")
async def reset_password(reset_data: ResetPasswordModel, response: Response):
    """
    Reset password using OTP
    
    - **email**: User's email address
    - **otp**: OTP received via email
    - **new_password**: New password
    """
    result = await auth_service.reset_password(
        email=reset_data.email,
        otp=reset_data.otp,
        new_password=reset_data.new_password
    )
    response.status_code = result.get("code", 200)
    return result

@router.post("/change-password")
async def change_password(change_data: ChangePasswordModel, response: Response, current_user: dict = Depends(permission_service.require_permission("password", "update"))):
    """
    Change password for authenticated user
    
    - **current_password**: Current password
    - **new_password**: New password
    """
    result = await auth_service.change_password(
        user_id=str(current_user["_id"]),
        current_password=change_data.current_password,
        new_password=change_data.new_password
    )
    response.status_code = result.get("code", 200)
    return result