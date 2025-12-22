from datetime import datetime
from typing import Optional, Dict, Any
from config.database import get_db
from core.auto_increment import get_next_sequence
from core.response import create_response
from core.query_params import QueryParams
from bson import ObjectId

class BaseService:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
    
    async def get_collection(self):
        db = await get_db()
        return db[self.collection_name]
    
    async def create(self, data: Dict[str, Any]) -> Dict:
        try:
            collection = await self.get_collection()
            doc = {
                "id": await get_next_sequence(self.collection_name),
                **data,
                "is_deleted": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            result = await collection.insert_one(doc)
            doc["_id"] = str(result.inserted_id)
            return create_response(
                message=f"{self.collection_name.capitalize()} created successfully",
                data=doc
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def get_all(self, query_params: Optional[QueryParams] = None) -> Dict:
        try:
            collection = await self.get_collection()
            query = {"is_deleted": False}
            
            if query_params:
                if query_params.filter:
                    query.update(query_params.parse_filter())
                
                if query_params.search:
                    search_query = query_params.parse_search()
                    if search_query:
                        query.update(search_query)
                
                projection = query_params.parse_select() if query_params.select else None
                sort_criteria = query_params.parse_sort() if query_params.sort else None
                
                total = await collection.count_documents(query)
                
                cursor = collection.find(query, projection)
                
                if sort_criteria:
                    cursor = cursor.sort(sort_criteria)
                
                if not query_params.no_limit:
                    cursor = cursor.skip(query_params.skip).limit(query_params.limit)
                    items = await cursor.to_list(query_params.limit)
                else:
                    items = await cursor.to_list(None)
                
                for item in items:
                    item["_id"] = str(item["_id"])
                
                meta = {
                    "skip": query_params.skip,
                    "limit": query_params.limit,
                    "count": len(items),
                    "total": total,
                    "filter": query_params.filter,
                    "select": query_params.select,
                    "sort": query_params.sort
                }
                
                return create_response(
                    message=f"{self.collection_name.capitalize()} retrieved successfully",
                    data=items,
                    meta=meta
                )
            else:
                items = await collection.find(query).sort("id", 1).to_list(None)
                for item in items:
                    item["_id"] = str(item["_id"])
                return create_response(
                    message=f"{self.collection_name.capitalize()} retrieved successfully",
                    data=items
                )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def get_by_id(self, item_id: int) -> Dict:
        try:
            collection = await self.get_collection()
            item = await collection.find_one({"id": item_id, "is_deleted": False})
            if not item:
                return create_response(
                    success=False,
                    code=404,
                    message=f"{self.collection_name.capitalize()} not found",
                    data=None
                )
            item["_id"] = str(item["_id"])
            return create_response(
                message=f"{self.collection_name.capitalize()} retrieved successfully",
                data=item
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def update(self, item_id: int, data: Dict[str, Any]) -> Dict:
        try:
            collection = await self.get_collection()
            item = await collection.find_one({"id": item_id, "is_deleted": False})
            if not item:
                return create_response(
                    success=False,
                    code=404,
                    message=f"{self.collection_name.capitalize()} not found",
                    data=None
                )
            
            update_data = {**data, "updated_at": datetime.utcnow()}
            await collection.update_one(
                {"id": item_id},
                {"$set": update_data}
            )
            
            return create_response(
                message=f"{self.collection_name.capitalize()} updated successfully",
                data=None
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
    
    async def delete(self, item_id: int) -> Dict:
        try:
            collection = await self.get_collection()
            item = await collection.find_one({"id": item_id, "is_deleted": False})
            if not item:
                return create_response(
                    success=False,
                    code=404,
                    message=f"{self.collection_name.capitalize()} not found",
                    data=None
                )
            
            await collection.update_one(
                {"id": item_id},
                {"$set": {"is_deleted": True, "updated_at": datetime.utcnow()}}
            )
            
            return create_response(
                message=f"{self.collection_name.capitalize()} deleted successfully",
                data=None
            )
        except Exception as e:
            return create_response(
                success=False,
                code=500,
                message=str(e),
                data=None
            )
