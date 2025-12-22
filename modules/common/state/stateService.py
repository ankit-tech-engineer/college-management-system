from datetime import datetime
from config.database import get_db
from core.response import create_response
from core.auto_increment import get_next_sequence
from core.query_params import QueryParams
from modules.common.state.stateModel import StateModel, StateUpdateModel
from bson import ObjectId

class StateService:
    async def get_collection(self):
        db = await get_db()
        return db["comm_states"]
    
    async def create_state(self, state_data: StateModel):
        try:
            collection = await self.get_collection()
            
            state_doc = {
                "id": await get_next_sequence("comm_states"),
                "name": state_data.name,
                "code": state_data.code,
                "country_id": state_data.country_id,
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.insert_one(state_doc)
            return create_response(message="State created successfully", data={"state_id": str(result.inserted_id)})
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_all_states(self):
        try:
            collection = await self.get_collection()
            states = await collection.find({"is_deleted": False}).to_list(None)
            
            states_list = [{
                "id": ["id"],
                "name": s["name"],
                "code": s["code"],
                "country_id": s["country_id"],
                "is_deleted": s.get("is_deleted", False),
                "created_at": s.get("created_at"),
                "updated_at": s.get("updated_at")
            } for s in states]
            
            return create_response(message="States retrieved successfully", data=states_list)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_states_by_country(self, country_id: str, query_params: QueryParams = None):
        try:
            collection = await self.get_collection()
            
            query = {"country_id": country_id, "is_deleted": False}
            if query_params and query_params.filter:
                query.update(query_params.filter)
            
            if query_params and query_params.search:
                query["$or"] = [
                    {"name": {"$regex": query_params.search, "$options": "i"}},
                    {"code": {"$regex": query_params.search, "$options": "i"}}
                ]
            
            cursor = collection.find(query)
            
            if query_params and query_params.sort:
                cursor = cursor.sort(list(query_params.sort.items()))
            
            if query_params and query_params.skip:
                cursor = cursor.skip(query_params.skip)
            
            if query_params and query_params.limit:
                cursor = cursor.limit(query_params.limit)
            
            states = await cursor.to_list(None if query_params and query_params.no_limit else 1000)
            total = await collection.count_documents(query)
            
            states_list = [{
                "id": s["id"],
                "name": s["name"],
                "code": s["code"],
                "country_id": s["country_id"],
                "is_deleted": s.get("is_deleted", False),
                "created_at": s.get("created_at"),
                "updated_at": s.get("updated_at")
            } for s in states]
            
            return create_response(
                message="States retrieved successfully",
                data=states_list,
                meta={
                    "skip": query_params.skip if query_params else 0,
                    "limit": query_params.limit if query_params else len(states_list),
                    "count": len(states_list),
                    "total": total,
                    "filter": query_params.filter if query_params else {},
                    "select": query_params.select if query_params else None,
                    "sort": query_params.sort if query_params else {"_id": -1}
                }
            )
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def update_state(self, state_id: str, state_data: StateUpdateModel):
        try:
            collection = await self.get_collection()
            update_data = {"updated_at": datetime.utcnow()}
            
            if state_data.name:
                update_data["name"] = state_data.name
            if state_data.code:
                update_data["code"] = state_data.code
            if state_data.country_id:
                update_data["country_id"] = state_data.country_id
            
            result = await collection.update_one(
                {"id": int(state_id), "is_deleted": False},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="State not found", data=None)
            
            return create_response(message="State updated successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def delete_state(self, state_id: str):
        try:
            collection = await self.get_collection()
            result = await collection.update_one(
                {"id": int(state_id), "is_deleted": False},
                {"$set": {"is_deleted": True, "updated_at": datetime.utcnow()}}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="State not found", data=None)
            
            return create_response(message="State deleted successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
