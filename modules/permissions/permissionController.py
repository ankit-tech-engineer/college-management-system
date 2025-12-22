from fastapi import APIRouter, Depends
from modules.permissions.permissionService import PermissionService
from modules.permissions.permissionModel import PermissionUpdateModel
from core.response import create_response
from core.query_params import QueryParams
from typing import List

router = APIRouter()
permission_service = PermissionService()

@router.get("/", tags=["Permissions"])
async def get_all_permissions(current_user: dict = Depends(permission_service.require_permission("permissions", "read"))):
    """Get all permissions for all roles"""
    from modules.roles.roleService import RoleService
    role_service = RoleService()
    return await role_service.get_all_roles()

@router.get("/check/{resource}/{action}", tags=["Permissions"])
async def check_permission(resource: str, action: str, current_user: dict = Depends(permission_service.require_permission("permissions", "read"))):
    """Check if current user has permission for resource and action"""
    user_role = current_user.get("role", "")
    has_permission = await permission_service.check_permission(user_role, resource, action)
    
    return create_response(
        message="Permission check completed",
        data={
            "resource": resource,
            "action": action,
            "has_permission": has_permission
        }
    )

@router.get("/role/{role_name}", tags=["Permissions"])
async def get_permissions_by_role(role_name: str, current_user: dict = Depends(permission_service.require_permission("permissions", "read"))):
    """Get all permissions for a specific role"""
    return await permission_service.get_permissions_by_role(role_name)

@router.put("/role/{role_name}", tags=["Permissions"])
async def update_permissions(role_name: str, permission_data: PermissionUpdateModel, current_user: dict = Depends(permission_service.require_permission("permissions", "update"))):
    """Update all permissions for a role"""
    return await permission_service.update_permissions(role_name, permission_data)

@router.post("/role/{role_name}/add", tags=["Permissions"])
async def add_permission(role_name: str, resource: str, actions: List[str], allowed_actions: List[str], current_user: dict = Depends(permission_service.require_permission("permissions", "create"))):
    """Add a single permission to a role"""
    return await permission_service.add_permission(role_name, resource, actions, allowed_actions)

@router.delete("/role/{role_name}/remove/{resource}", tags=["Permissions"])
async def remove_permission(role_name: str, resource: str, current_user: dict = Depends(permission_service.require_permission("permissions", "delete"))):
    """Remove a permission from a role"""
    return await permission_service.remove_permission(role_name, resource)
