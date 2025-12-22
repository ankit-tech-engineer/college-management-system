from pydantic import BaseModel
from typing import Optional

class ProgramCreateSchema(BaseModel):
    program_name: str
    short_name: Optional[str] = None
    level: str
    duration_years: int
    status: Optional[str] = "active"

class ProgramUpdateSchema(BaseModel):
    program_name: Optional[str] = None
    short_name: Optional[str] = None
    level: Optional[str] = None
    duration_years: Optional[int] = None
    status: Optional[str] = None
