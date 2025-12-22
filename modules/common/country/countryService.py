from datetime import datetime
from config.database import get_db
from core.response import create_response
from core.auto_increment import get_next_sequence
from core.query_params import QueryParams
from modules.common.country.countryModel import CountryModel, CountryUpdateModel
from bson import ObjectId

class CountryService:
    async def get_collection(self):
        db = await get_db()
        return db["comm_countries"]
    
    async def create_country(self, country_data: CountryModel):
        try:
            collection = await self.get_collection()
            
            existing = await collection.find_one({"code": country_data.code, "is_deleted": False})
            if existing:
                return create_response(success=False, code=400, message="Country already exists", data=None)
            
            country_doc = {
                "id": await get_next_sequence("comm_countries"),
                "name": country_data.name,
                "code": country_data.code,
                "phone_code": country_data.phone_code,
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            result = await collection.insert_one(country_doc)
            return create_response(message="Country created successfully", data={"country_id": str(result.inserted_id)})
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_all_countries(self):
        try:
            collection = await self.get_collection()
            countries = await collection.find({"is_deleted": False}).to_list(None)
            countries_list = [{
                "id": c["id"],
                "name": c["name"],
                "code": c["code"],
                "phone_code": c.get("phone_code"),
                "is_deleted": c.get("is_deleted", False),
                "created_at": c.get("created_at"),
                "updated_at": c.get("updated_at")
            } for c in countries]
            
            return create_response(message="Countries retrieved successfully", data=countries_list)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def get_country_by_id(self, country_id: str, query_params: QueryParams = None):
        try:
            collection = await self.get_collection()
            country = await collection.find_one({"id": int(country_id), "is_deleted": False})
            
            if not country:
                return create_response(success=False, code=404, message="Country not found", data=None)
            
            return create_response(
                message="Country retrieved successfully",
                data={
                    "id": country["id"],
                    "name": country["name"],
                    "code": country["code"],
                    "phone_code": country.get("phone_code"),
                    "is_deleted": country.get("is_deleted", False),
                    "created_at": country.get("created_at"),
                    "updated_at": country.get("updated_at")
                },
                meta={
                    "skip": query_params.skip if query_params else 0,
                    "limit": query_params.limit if query_params else 1,
                    "count": 1,
                    "total": 1,
                    "filter": query_params.filter if query_params else {},
                    "select": query_params.select if query_params else None,
                    "sort": query_params.sort if query_params else {"_id": -1}
                }
            )
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def update_country(self, country_id: str, country_data: CountryUpdateModel):
        try:
            collection = await self.get_collection()
            update_data = {"updated_at": datetime.utcnow()}
            
            if country_data.name:
                update_data["name"] = country_data.name
            if country_data.code:
                update_data["code"] = country_data.code
            if country_data.phone_code:
                update_data["phone_code"] = country_data.phone_code
            
            result = await collection.update_one(
                {"id": int(country_id), "is_deleted": False},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="Country not found", data=None)
            
            return create_response(message="Country updated successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
    
    async def delete_country(self, country_id: str):
        try:
            collection = await self.get_collection()
            result = await collection.update_one(
                {"id": int(country_id), "is_deleted": False},
                {"$set": {"is_deleted": True, "updated_at": datetime.utcnow()}}
            )
            
            if result.matched_count == 0:
                return create_response(success=False, code=404, message="Country not found", data=None)
            
            return create_response(message="Country deleted successfully", data=None)
        except Exception as e:
            return create_response(success=False, code=500, message=str(e), data=None)
