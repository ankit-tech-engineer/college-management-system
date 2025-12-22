from pydantic import BaseModel
from typing import List, Optional

class PermissionItemModel(BaseModel):
    resource: str
    actions: List[str]
    allowed_actions: List[str]

class PermissionModel(BaseModel):
    role: str
    permissions: List[PermissionItemModel]

class PermissionUpdateModel(BaseModel):
    permissions: List[PermissionItemModel]
