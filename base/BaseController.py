from fastapi import APIRouter, Response, Depends, Query
from typing import Type, Optional
from base.BaseService import BaseService
from base.BaseSchema import CreateSchema, UpdateSchema
from modules.permissions.permissionService import PermissionService
from core.query_params import QueryParams

class BaseController:
    def __init__(self, service: BaseService, create_schema: Type[CreateSchema], update_schema: Type[UpdateSchema], resource_name: str):
        self.service = service
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.resource_name = resource_name
        self.permission_service = PermissionService()
        self.router = APIRouter()
    
    def create_routes(self):
        @self.router.post("/")
        async def create(data: self.create_schema, response: Response, current_user: dict = Depends(self.permission_service.require_permission(self.resource_name, "create"))):
            result = await self.service.create(data.dict(exclude_unset=True))
            response.status_code = result.get("code", 200)
            return result
        
        @self.router.get("/")
        async def get_all(
            response: Response,
            skip: int = Query(0, ge=0),
            limit: int = Query(10, ge=1, le=100),
            sort: Optional[str] = Query(None),
            filter: Optional[str] = Query(None),
            search: Optional[str] = Query(None),
            select: Optional[str] = Query(None),
            no_limit: bool = Query(False),
            current_user: dict = Depends(self.permission_service.require_permission(self.resource_name, "read"))
        ):
            query_params = QueryParams(skip=skip, limit=limit, sort=sort, filter=filter, search=search, select=select, no_limit=no_limit)
            result = await self.service.get_all(query_params)
            response.status_code = result.get("code", 200)
            return result
        
        @self.router.get("/{item_id}")
        async def get_by_id(item_id: int, response: Response, current_user: dict = Depends(self.permission_service.require_permission(self.resource_name, "read"))):
            result = await self.service.get_by_id(item_id)
            response.status_code = result.get("code", 200)
            return result
        
        @self.router.put("/{item_id}")
        async def update(item_id: int, data: self.update_schema, response: Response, current_user: dict = Depends(self.permission_service.require_permission(self.resource_name, "update"))):
            result = await self.service.update(item_id, data.dict(exclude_unset=True))
            response.status_code = result.get("code", 200)
            return result
        
        @self.router.delete("/{item_id}")
        async def delete(item_id: int, response: Response, current_user: dict = Depends(self.permission_service.require_permission(self.resource_name, "delete"))):
            result = await self.service.delete(item_id)
            response.status_code = result.get("code", 200)
            return result
        
        return self.router
