from fastapi import APIRouter, Depends
from modules.common.state.stateService import StateService
from modules.common.state.stateModel import StateModel, StateUpdateModel
from modules.permissions.permissionService import PermissionService
from core.query_params import QueryParams

router = APIRouter()
state_service = StateService()
permission_service = PermissionService()

@router.post("/", tags=["States"])
async def create_state(state_data: StateModel, current_user: dict = Depends(permission_service.require_permission("states", "create"))):
    return await state_service.create_state(state_data)

@router.get("/", tags=["States"])
async def get_all_states(current_user: dict = Depends(permission_service.require_permission("states", "read"))):
    return await state_service.get_all_states()

@router.get("/country/{country_id}", tags=["States"])
async def get_states_by_country(country_id: str, query_params: QueryParams = Depends(), current_user: dict = Depends(permission_service.require_permission("states", "read"))):
    return await state_service.get_states_by_country(country_id, query_params)

@router.put("/{state_id}", tags=["States"])
async def update_state(state_id: str, state_data: StateUpdateModel, current_user: dict = Depends(permission_service.require_permission("states", "update"))):
    return await state_service.update_state(state_id, state_data)

@router.delete("/{state_id}", tags=["States"])
async def delete_state(state_id: str, current_user: dict = Depends(permission_service.require_permission("states", "delete"))):
    return await state_service.delete_state(state_id)
