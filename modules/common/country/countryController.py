from fastapi import APIRouter, Depends
from modules.common.country.countryService import CountryService
from modules.common.country.countryModel import CountryModel, CountryUpdateModel
from modules.permissions.permissionService import PermissionService
from core.query_params import QueryParams

router = APIRouter()
country_service = CountryService()
permission_service = PermissionService()

@router.post("/", tags=["Countries"])
async def create_country(country_data: CountryModel, current_user: dict = Depends(permission_service.require_permission("countries", "create"))):
    return await country_service.create_country(country_data)

@router.get("/", tags=["Countries"])
async def get_all_countries(current_user: dict = Depends(permission_service.require_permission("countries", "read"))):
    return await country_service.get_all_countries()

@router.get("/{country_id}", tags=["Countries"])
async def get_country(country_id: str, query_params: QueryParams = Depends(), current_user: dict = Depends(permission_service.require_permission("countries", "read"))):
    return await country_service.get_country_by_id(country_id, query_params)

@router.put("/{country_id}", tags=["Countries"])
async def update_country(country_id: str, country_data: CountryUpdateModel, current_user: dict = Depends(permission_service.require_permission("countries", "update"))):
    return await country_service.update_country(country_id, country_data)

@router.delete("/{country_id}", tags=["Countries"])
async def delete_country(country_id: str, current_user: dict = Depends(permission_service.require_permission("countries", "delete"))):
    return await country_service.delete_country(country_id)
