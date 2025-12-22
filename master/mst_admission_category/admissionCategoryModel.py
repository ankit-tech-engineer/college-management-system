from pydantic import BaseModel
from typing import Optional

class AdmissionCategoryCreateSchema(BaseModel):
    category_name: str
    description: Optional[str] = None
    status: Optional[str] = "active"

class AdmissionCategoryUpdateSchema(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
