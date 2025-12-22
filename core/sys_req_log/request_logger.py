from datetime import datetime
from fastapi import Request
from config.database import get_db
from core.auto_increment import get_next_sequence

async def log_request(request: Request, response_status: int, response_body: dict = None):
    """Log request details to sys_req_log collection"""
    try:
        db = await get_db()
        collection = db["sys_req_log"]
        
        log_doc = {
            "id": await get_next_sequence("sys_req_log"),
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "client_host": request.client.host if request.client else None,
            "response_status": response_status,
            "response_body": response_body,
            "timestamp": datetime.utcnow()
        }
        
        await collection.insert_one(log_doc)
    except Exception as e:
        print(f"Error logging request: {str(e)}")
