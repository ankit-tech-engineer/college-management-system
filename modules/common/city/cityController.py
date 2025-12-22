from fastapi import APIRouter, Depends
from modules.common.city.cityService import CityService
from modules.common.city.cityModel import CityModel, CityUpdateModel
from modules.permissions.permissionService import PermissionService
from core.query_params import QueryParams

router = APIRouter()
city_service = CityService()
permission_service = PermissionService()

@router.post("/", tags=["Cities"])
async def create_city(city_data: CityModel, current_user: dict = Depends(permission_service.require_permission("cities", "create"))):
    return await city_service.create_city(city_data)

@router.get("/", tags=["Cities"])
async def get_all_cities(current_user: dict = Depends(permission_service.require_permission("cities", "read"))):
    return await city_service.get_all_cities()

@router.get("/state/{state_id}", tags=["Cities"])
async def get_cities_by_state(state_id: str, query_params: QueryParams = Depends(), current_user: dict = Depends(permission_service.require_permission("cities", "read"))):
    return await city_service.get_cities_by_state(state_id, query_params)

@router.put("/{city_id}", tags=["Cities"])
async def update_city(city_id: str, city_data: CityUpdateModel, current_user: dict = Depends(permission_service.require_permission("cities", "update"))):
    return await city_service.update_city(city_id, city_data)

@router.delete("/{city_id}", tags=["Cities"])
async def delete_city(city_id: str, current_user: dict = Depends(permission_service.require_permission("cities", "delete"))):
    return await city_service.delete_city(city_id)
