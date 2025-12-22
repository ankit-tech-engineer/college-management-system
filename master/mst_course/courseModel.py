from pydantic import BaseModel
from typing import Optional

class CourseCreateSchema(BaseModel):
    course_name: str
    course_code: Optional[str] = None
    credits: Optional[int] = None
    department_id: int
    status: Optional[str] = "active"

class CourseUpdateSchema(BaseModel):
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None
    status: Optional[str] = None
