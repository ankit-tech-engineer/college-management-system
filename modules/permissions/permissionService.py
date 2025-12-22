from fastapi import HTTPException, status, Depends
from modules.roles.roleService import RoleService
from modules.auth.dependencies import get_current_user, AuthException
from config.database import get_db
from core.response import create_response
from modules.permissions.permissionModel import PermissionUpdateModel
from datetime import datetime

class PermissionService:
    def __init__(self):
        self.role_service = RoleService()
    
    async def get_collection(self):
        db = await get_db()
        return db["roles"]
    
    async def check_permission(self, user_role: str, resource: str, action: str) -> bool:
        """Check if user role has permission for resource and action"""
        try:
            role_data = await self.role_service.get_role_by_name(user_role)
            if not role_data:
                return False
            
            permissions = role_data.get("permissions", [])
            for perm in permissions:
                if perm.get("resource") == resource:
                    return action in perm.get("allowed_actions", [])
            
            return False
        except:
            return False
    
    def require_permission(self, resource: str, action: str):
        """Dependency to check permission for resource and action"""
        async def permission_checker(current_user: dict = Depends(get_current_user)):
            user_role = current_user.get("role", "")
            has_permission = await self.check_permission(user_role, resource, action)
            
            if not has_permission:
                raise AuthException(f"Permission denied: {resource}.{action}", 403)
            
            return current_user
        return permission_checker
    
    async def get_permissions_by_role(self, role_name: str):
        """Get permissions for a specific role"""
        try:
            collection = await self.get_collection()
            role = await collection.find_one({"role": role_name, "is_deleted": False})
            
            if not role:
                return create_response(success=False, code=404, message="Role not found", data=None)
            
            return create_response(message="Permissions retrieved successfully", data={
                "role": role["role"],
                "permissions": role.get("permissions", [])
            })
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def update_permissions(self, role_name: str, permission_data: PermissionUpdateModel):
        """Update permissions for a role"""
        try:
            collection = await self.get_collection()
            
            permissions_list = [{
                "resource": perm.resource,
                "actions": perm.actions,
                "allowed_actions": perm.allowed_actions
            } for perm in permission_data.permissions]
            
            result = await collection.update_one(
                {"role": role_name, "is_deleted": False},
                {"$set": {"permissions": permissions_list, "updated_at": datetime.utcnow()}}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="Role not found", data=None)
            
            return create_response(message="Permissions updated successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def add_permission(self, role_name: str, resource: str, actions: list, allowed_actions: list):
        """Add a single permission to a role"""
        try:
            collection = await self.get_collection()
            role = await collection.find_one({"role": role_name, "is_deleted": False})
            
            if not role:
                return create_response(success=False, code=404, message="Role not found", data=None)
            
            permissions = role.get("permissions", [])
            
            # Check if permission already exists
            for perm in permissions:
                if perm.get("resource") == resource:
                    return create_response(success=False, code=400, message="Permission already exists for this resource", data=None)
            
            permissions.append({
                "resource": resource,
                "actions": actions,
                "allowed_actions": allowed_actions
            })
            
            await collection.update_one(
                {"role": role_name, "is_deleted": False},
                {"$set": {"permissions": permissions, "updated_at": datetime.utcnow()}}
            )
            
            return create_response(message="Permission added successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def remove_permission(self, role_name: str, resource: str):
        """Remove a permission from a role"""
        try:
            collection = await self.get_collection()
            role = await collection.find_one({"role": role_name, "is_deleted": False})
            
            if not role:
                return create_response(success=False, code=404, message="Role not found", data=None)
            
            permissions = role.get("permissions", [])
            permissions = [p for p in permissions if p.get("resource") != resource]
            
            await collection.update_one(
                {"role": role_name, "is_deleted": False},
                {"$set": {"permissions": permissions, "updated_at": datetime.utcnow()}}
            )
            
            return create_response(message="Permission removed successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
