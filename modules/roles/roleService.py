from datetime import datetime
from config.database import get_db
from core.response import create_response
from modules.roles.roleModel import RoleModel, RoleUpdateModel
from core.auto_increment import get_next_sequence
from core.query_params import QueryParams
from bson import ObjectId

class RoleService:
    def __init__(self):
        pass
    
    async def get_collection(self):
        db = await get_db()
        return db["roles"]
    
    async def create_role(self, role_data: RoleModel):
        """Create a new role"""
        try:
            collection = await self.get_collection()
            
            # Check if role already exists
            existing = await collection.find_one({"role": role_data.role})
            if existing:
                return create_response(
                    success=False,
                    code=400,
                    message="Role already exists",
                    data=None
                )
            
            permissions_list = [
                {
                    "resource": perm.resource,
                    "actions": perm.actions,
                    "allowed_actions": perm.allowed_actions
                }
                for perm in role_data.permissions
            ]
            
            role_doc = {
                "id": await get_next_sequence("roles"),
                "role": role_data.role,
                "permissions": permissions_list,
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.insert_one(role_doc)
            return create_response(
                message="Role created successfully",
                data={
                    "role_id": str(result.inserted_id),
                    "role": role_data.role
                }
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def get_all_roles(self):
        """Get all active roles"""
        try:
            collection = await self.get_collection()
            roles = await collection.find({"is_deleted": False}).to_list(None)
            
            roles_list = [{
                "id":role["id"],
                "role": role["role"],
                "permissions": role.get("permissions", []),
                "is_deleted": role.get("is_deleted", False),
                "created_at": role.get("created_at"),
                "updated_at": role.get("updated_at")
            } for role in roles]
            
            return create_response(
                message="Roles retrieved successfully",
                data=roles_list
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def get_role_by_name(self, role_name: str):
        """Get role by name (internal use)"""
        try:
            collection = await self.get_collection()
            role = await collection.find_one({"role": role_name, "is_deleted": False})
            
            if not role:
                return None
            
            return {
                "id": role["_id"],
                "role": role["role"],
                "permissions": role.get("permissions", [])
            }
        except Exception as e:
            return None
    
    async def get_role_by_role(self, role_name: str):
        """Get role by name (API endpoint)"""
        try:
            collection = await self.get_collection()
            role = await collection.find_one({"role": role_name, "is_deleted": False})
            
            if not role:
                return create_response(success=False, code=404, message="Role not found", data=None)
            
            return create_response(message="Role retrieved successfully", data={
                "id": role["id"],
                "role": role["role"],
                "permissions": role.get("permissions", []),
                "is_deleted": role.get("is_deleted", False),
                "created_at": role.get("created_at"),
                "updated_at": role.get("updated_at")
            })
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def update_role(self, role_id: str, role_data: RoleUpdateModel):
        """Update role"""
        try:
            collection = await self.get_collection()
            
            update_data = {"updated_at": datetime.utcnow()}
            if role_data.role:
                update_data["role"] = role_data.role
            if role_data.permissions is not None:
                permissions_list = [
                    {
                        "resource": perm.resource,
                        "actions": perm.actions,
                        "allowed_actions": perm.allowed_actions
                    }
                    for perm in role_data.permissions
                ]
                update_data["permissions"] = permissions_list
            
            result = await collection.update_one(
                {"id": int(role_id), "is_deleted": False},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return create_response(
                    success=False,
                    code=404,
                    message="Role not found",
                    data=None
                )
            
            return create_response(
                message="Role updated successfully",
                data=None
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def delete_role(self, role_id: str):
        """Soft delete role"""
        try:
            collection = await self.get_collection()
            
            result = await collection.update_one(
                {"id": int(role_id), "is_deleted": False},
                {"$set": {
                    "is_deleted": True,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            if result.matched_count == 0:
                return create_response(
                    success=False,
                    code=404,
                    message="Role not found",
                    data=None
                )
            
            return create_response(
                message="Role deleted successfully",
                data=None
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )