from pydantic import BaseModel
from typing import List, Optional

class PermissionModel(BaseModel):
    resource: str
    actions: List[str]
    allowed_actions: List[str]

class RoleModel(BaseModel):
    role: str
    permissions: List[PermissionModel] = []

class RoleUpdateModel(BaseModel):
    role: Optional[str] = None
    permissions: Optional[List[PermissionModel]] = None