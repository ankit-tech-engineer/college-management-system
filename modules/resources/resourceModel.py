from pydantic import BaseModel
from typing import List, Optional

class ResourceModel(BaseModel):
    name: str
    actions: List[str]

class ResourceUpdateModel(BaseModel):
    name: Optional[str] = None
    actions: Optional[List[str]] = None
