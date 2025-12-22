from datetime import datetime
from config.database import get_db
from core.response import create_response
from core.auto_increment import get_next_sequence
from core.query_params import QueryParams
from modules.common.city.cityModel import CityModel, CityUpdateModel
from bson import ObjectId

class CityService:
    async def get_collection(self):
        db = await get_db()
        return db["comm_cities"]
    
    async def create_city(self, city_data: CityModel):
        try:
            collection = await self.get_collection()
            
            city_doc = {
                "id": await get_next_sequence("comm_cities"),
                "name": city_data.name,
                "state_id": city_data.state_id,
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.insert_one(city_doc)
            return create_response(message="City created successfully", data={"city_id": str(result.inserted_id)})
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_all_cities(self):
        try:
            collection = await self.get_collection()
            cities = await collection.find({"is_deleted": False}).to_list(None)
            
            cities_list = [{
                "id": ["id"],
                "name": c["name"],
                "state_id": c["state_id"],
                "is_deleted": c.get("is_deleted", False),
                "created_at": c.get("created_at"),
                "updated_at": c.get("updated_at")
            } for c in cities]
            
            return create_response(message="Cities retrieved successfully", data=cities_list)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_cities_by_state(self, state_id: str, query_params: QueryParams = None):
        try:
            collection = await self.get_collection()
            
            query = {"state_id": state_id, "is_deleted": False}
            if query_params and query_params.filter:
                query.update(query_params.filter)
            
            if query_params and query_params.search:
                query["name"] = {"$regex": query_params.search, "$options": "i"}
            
            cursor = collection.find(query)
            
            if query_params and query_params.sort:
                cursor = cursor.sort(list(query_params.sort.items()))
            
            if query_params and query_params.skip:
                cursor = cursor.skip(query_params.skip)
            
            if query_params and query_params.limit:
                cursor = cursor.limit(query_params.limit)
            
            cities = await cursor.to_list(None if query_params and query_params.no_limit else 1000)
            total = await collection.count_documents(query)
            
            cities_list = [{
                "id": ["id"],
                "name": c["name"],
                "state_id": c["state_id"],
                "is_deleted": c.get("is_deleted", False),
                "created_at": c.get("created_at"),
                "updated_at": c.get("updated_at")
            } for c in cities]
            
            return create_response(
                message="Cities retrieved successfully",
                data=cities_list,
                meta={
                    "skip": query_params.skip if query_params else 0,
                    "limit": query_params.limit if query_params else len(cities_list),
                    "count": len(cities_list),
                    "total": total,
                    "filter": query_params.filter if query_params else {},
                    "select": query_params.select if query_params else None,
                    "sort": query_params.sort if query_params else {"_id": -1}
                }
            )
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def update_city(self, city_id: str, city_data: CityUpdateModel):
        try:
            collection = await self.get_collection()
            update_data = {"updated_at": datetime.utcnow()}
            
            if city_data.name:
                update_data["name"] = city_data.name
            if city_data.state_id:
                update_data["state_id"] = city_data.state_id
            
            result = await collection.update_one(
                {"id": int(city_id), "is_deleted": False},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="City not found", data=None)
            
            return create_response(message="City updated successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def delete_city(self, city_id: str):
        try:
            collection = await self.get_collection()
            result = await collection.update_one(
                {"id": int(city_id), "is_deleted": False},
                {"$set": {"is_deleted": True, "updated_at": datetime.utcnow()}}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="City not found", data=None)
            
            return create_response(message="City deleted successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
