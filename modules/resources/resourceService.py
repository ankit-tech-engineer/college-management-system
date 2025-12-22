from datetime import datetime
from config.database import get_db
from core.response import create_response
from core.auto_increment import get_next_sequence
from core.query_params import QueryParams
from modules.resources.resourceModel import ResourceModel, ResourceUpdateModel
from bson import ObjectId

class ResourceService:
    def __init__(self):
        pass
    
    async def get_collection(self):
        db = await get_db()
        return db["resources"]
    
    def generate_key(self, name: str) -> str:
        """Generate key from name by replacing spaces with underscores and converting to lowercase"""
        return name.strip().replace(" ", "_").lower()
    
    async def create_resource(self, resource_data: ResourceModel):
        """Create a new resource"""
        try:
            collection = await self.get_collection()
            key = self.generate_key(resource_data.name)
            
            existing = await collection.find_one({"key": key, "is_deleted": False})
            if existing:
                return create_response(success=False, code=400, message="Resource already exists", data=None)
            
            resource_doc = {
                "id": await get_next_sequence("resources"),
                "key": key,
                "name": resource_data.name,
                "actions": resource_data.actions,
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.insert_one(resource_doc)
            return create_response(message="Resource created successfully", data={"resource_id": str(result.inserted_id), "key": key})
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_all_resources(self):
        """Get all active resources"""
        try:
            collection = await self.get_collection()
            resources = await collection.find({"is_deleted": False}).to_list(None)
            
            resources_list = [{
                "id": r["id"],
                "key": r["key"],
                "name": r["name"],
                "actions": r["actions"],
                "is_deleted": r.get("is_deleted", False),
                "created_at": r.get("created_at"),
                "updated_at": r.get("updated_at")
            } for r in resources]
            
            return create_response(message="Resources retrieved successfully", data=resources_list)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_resource_by_key(self, key: str):
        """Get resource by key"""
        try:
            collection = await self.get_collection()
            resource = await collection.find_one({"key": key, "is_deleted": False})
            
            if not resource:
                return create_response(success=False, code=404, message="Resource not found", data=None)
            
            return create_response(message="Resource retrieved successfully", data={
                "id": resource["id"],
                "key": resource["key"],
                "name": resource["name"],
                "actions": resource["actions"],
                "is_deleted": resource.get("is_deleted", False),
                "created_at": resource.get("created_at"),
                "updated_at": resource.get("updated_at")
            })
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def update_resource(self, resource_id: str, resource_data: ResourceUpdateModel):
        """Update resource"""
        try:
            collection = await self.get_collection()
            update_data = {"updated_at": datetime.utcnow()}
            
            if resource_data.name:
                update_data["name"] = resource_data.name
                update_data["key"] = self.generate_key(resource_data.name)
            if resource_data.actions is not None:
                update_data["actions"] = resource_data.actions
            
            result = await collection.update_one(
                {"id": int(resource_id), "is_deleted": False},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="Resource not found", data=None)
            
            return create_response(message="Resource updated successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def delete_resource(self, resource_id: str):
        """Soft delete resource"""
        try:
            collection = await self.get_collection()
            result = await collection.update_one(
                {"id": int(resource_id), "is_deleted": False},
                {"$set": {"is_deleted": True, "updated_at": datetime.utcnow()}}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="Resource not found", data=None)
            
            return create_response(message="Resource deleted successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_resources_dict(self):
        """Get resources as dictionary for permission checking"""
        try:
            collection = await self.get_collection()
            resources = await collection.find({"is_deleted": False}).to_list(None)
            return {r["key"]: r["actions"] for r in resources}
        except:
            return {}
