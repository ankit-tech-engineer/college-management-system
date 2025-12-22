from fastapi import APIRouter, Depends
from modules.permissions.permissionService import PermissionService

router = APIRouter()
permission_service = PermissionService()

@router.get("/", tags=["Users"])
async def get_all_users(current_user: dict = Depends(permission_service.require_permission("users", "read"))):
    """
    Get all users
    """
    return {"message": "Get all users"}

@router.post("/", tags=["Users"])
async def create_user(current_user: dict = Depends(permission_service.require_permission("users", "create"))):
    """
    Create a new user
    """
    return {"message": "Create user"}

@router.get("/{user_id}", tags=["Users"])
async def get_user(user_id: str, current_user: dict = Depends(permission_service.require_permission("users", "read"))):
    """
    Get user by ID
    """
    return {"message": f"Get user {user_id}"}

@router.put("/{user_id}", tags=["Users"])
async def update_user(user_id: str, current_user: dict = Depends(permission_service.require_permission("users", "update"))):
    """
    Update user
    """
    return {"message": f"Update user {user_id}"}

@router.delete("/{user_id}", tags=["Users"])
async def delete_user(user_id: str, current_user: dict = Depends(permission_service.require_permission("users", "delete"))):
    """
    Delete user
    """
    return {"message": f"Delete user {user_id}"}
