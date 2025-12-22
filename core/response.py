from typing import Any, Optional, Dict

def create_response(
    success: bool = True,
    code: int = 200,
    message: Optional[str] = None,
    data: Any = None,
    meta: Optional[Dict] = None
) -> Dict[str, Any]:
    """Create standardized API response"""
    return {
        "success": success,
        "code": code,
        "meta": meta or {},
        "message": message,
        "data": data or []
    }