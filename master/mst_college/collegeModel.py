from pydantic import BaseModel
from typing import Optional

class CollegeCreateSchema(BaseModel):
    college_name: str
    short_name: Optional[str] = None
    status: Optional[str] = "active"

class CollegeUpdateSchema(BaseModel):
    college_name: Optional[str] = None
    short_name: Optional[str] = None
    status: Optional[str] = None
