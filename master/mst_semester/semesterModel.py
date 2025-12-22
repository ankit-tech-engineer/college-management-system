from pydantic import BaseModel
from typing import Optional

class SemesterCreateSchema(BaseModel):
    semester_number: int
    semester_name: Optional[str] = None
    program_id: int
    status: Optional[str] = "active"

class SemesterUpdateSchema(BaseModel):
    semester_number: Optional[int] = None
    semester_name: Optional[str] = None
    program_id: Optional[int] = None
    status: Optional[str] = None
