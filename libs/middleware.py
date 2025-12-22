from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.sys_req_log.request_logger import log_request
import json

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Log the request asynchronously
        try:
            await log_request(request, response.status_code)
        except Exception as e:
            print(f"Failed to log request: {str(e)}")
        
        return response
