from pydantic import BaseModel
from typing import Optional

class DepartmentCreateSchema(BaseModel):
    department_name: str
    short_name: Optional[str] = None
    college_id: int
    status: Optional[str] = "active"

class DepartmentUpdateSchema(BaseModel):
    department_name: Optional[str] = None
    short_name: Optional[str] = None
    college_id: Optional[int] = None
    status: Optional[str] = None
