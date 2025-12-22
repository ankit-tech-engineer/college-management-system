from fastapi import APIRouter, Response, Depends, Query
from typing import Optional
from config.database import get_db
from core.response import create_response
from core.query_params import QueryParams
from modules.permissions.permissionService import PermissionService

router = APIRouter()
permission_service = PermissionService()

@router.get("/request-logs")
async def get_request_logs(
    response: Response,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort: Optional[str] = Query(None),
    filter: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    select: Optional[str] = Query(None),
    no_limit: bool = Query(False),
    current_user: dict = Depends(permission_service.require_permission("request_logs", "read"))
):
    """Get request logs (super-admin only)"""
    try:
        if current_user.get("role") != "super-admin":
            return create_response(
                success=False,
                code=403,
                message="Access denied. Super-admin only.",
                data=None
            )
        
        db = await get_db()
        collection = db["sys_req_log"]
        query = {}
        
        query_params = QueryParams(skip=skip, limit=limit, sort=sort, filter=filter, search=search, select=select, no_limit=no_limit)
        
        if query_params.filter:
            query.update(query_params.parse_filter())
        
        if query_params.search:
            search_query = query_params.parse_search()
            if search_query:
                query.update(search_query)
        
        projection = query_params.parse_select() if query_params.select else None
        sort_criteria = query_params.parse_sort() if query_params.sort else [("timestamp", -1)]
        
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
        
        result = create_response(
            message="Request logs retrieved successfully",
            data=items,
            meta=meta
        )
        response.status_code = result.get("code", 200)
        return result
    except Exception as e:
        result = create_response(
            success=False,
            code=500,
            message=str(e),
            data=None
        )
        response.status_code = result.get("code", 500)
        return result
