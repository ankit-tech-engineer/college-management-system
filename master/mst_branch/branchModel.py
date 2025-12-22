from pydantic import BaseModel
from typing import Optional

class BranchCreateSchema(BaseModel):
    branch_name: str
    short_name: Optional[str] = None
    department_id: int
    status: Optional[str] = "active"

class BranchUpdateSchema(BaseModel):
    branch_name: Optional[str] = None
    short_name: Optional[str] = None
    department_id: Optional[int] = None
    status: Optional[str] = None
