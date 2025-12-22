from fastapi import APIRouter, Depends
from modules.resources.resourceService import ResourceService
from modules.resources.resourceModel import ResourceModel, ResourceUpdateModel
from modules.permissions.permissionService import PermissionService
from core.query_params import QueryParams

router = APIRouter()
resource_service = ResourceService()
permission_service = PermissionService()

@router.post("/", tags=["Resources"])
async def create_resource(resource_data: ResourceModel, current_user: dict = Depends(permission_service.require_permission("resources", "create"))):
    """Create a new resource"""
    return await resource_service.create_resource(resource_data)

@router.get("/", tags=["Resources"])
async def get_all_resources(current_user: dict = Depends(permission_service.require_permission("resources", "read"))):
    """Get all resources"""
    return await resource_service.get_all_resources()

@router.get("/resource/{key}", tags=["Resources"])
async def get_resource(key: str, query_params: QueryParams = Depends(), current_user: dict = Depends(permission_service.require_permission("resources", "read"))):
    """Get resource by key with pagination, filtering, sorting, and search"""
    return await resource_service.get_resource_by_key(key)

@router.put("/{resource_id}", tags=["Resources"])
async def update_resource(resource_id: str, resource_data: ResourceUpdateModel, current_user: dict = Depends(permission_service.require_permission("resources", "update"))):
    """Update resource"""
    return await resource_service.update_resource(resource_id, resource_data)

@router.delete("/{resource_id}", tags=["Resources"])
async def delete_resource(resource_id: str, current_user: dict = Depends(permission_service.require_permission("resources", "delete"))):
    """Delete resource"""
    return await resource_service.delete_resource(resource_id)
