from pydantic import BaseModel
from typing import List
from datetime import datetime

class ResourceResponse(BaseModel):
    id: str
    key: str
    name: str
    actions: List[str]
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
