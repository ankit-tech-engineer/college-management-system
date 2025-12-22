from pydantic import BaseModel
from typing import Optional

class DesignationCreateSchema(BaseModel):
    designation_name: str
    level: Optional[str] = None
    status: Optional[str] = "active"

class DesignationUpdateSchema(BaseModel):
    designation_name: Optional[str] = None
    level: Optional[str] = None
    status: Optional[str] = None
