from fastapi import APIRouter, Depends
from modules.roles.roleModel import RoleModel, RoleUpdateModel
from modules.roles.roleService import RoleService
from modules.permissions.permissionService import PermissionService
from core.query_params import QueryParams

router = APIRouter()
role_service = RoleService()
permission_service = PermissionService()

@router.post("/", tags=["Roles"])
async def create_role(role_data: RoleModel, current_user: dict = Depends(permission_service.require_permission("roles", "create"))):
    """
    Create a new role
    """
    result = await role_service.create_role(role_data)
    return result

@router.get("/", tags=["Roles"])
async def get_all_roles(current_user: dict = Depends(permission_service.require_permission("roles", "read"))):
    """
    Get all roles
    """
    result = await role_service.get_all_roles()
    return result

@router.get("/role/{role_name}", tags=["Roles"])
async def get_role_by_role(role_name: str, query_params: QueryParams = Depends(), current_user: dict = Depends(permission_service.require_permission("roles", "read"))):
    """
    Get role by name with pagination, filtering, sorting, and search
    """
    result = await role_service.get_role_by_role(role_name)
    return result

@router.put("/{role_id}", tags=["Roles"])
async def update_role(role_id: str, role_data: RoleUpdateModel, current_user: dict = Depends(permission_service.require_permission("roles", "update"))):
    """
    Update role
    """
    result = await role_service.update_role(role_id, role_data)
    return result

@router.delete("/{role_id}", tags=["Roles"])
async def delete_role(role_id: str, current_user: dict = Depends(permission_service.require_permission("roles", "delete"))):
    """
    Delete role
    """
    result = await role_service.delete_role(role_id)
    return result