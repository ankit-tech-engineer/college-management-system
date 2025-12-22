from pydantic import BaseModel
from typing import Optional

class DocumentTypeCreateSchema(BaseModel):
    document_name: str
    description: Optional[str] = None
    is_mandatory: Optional[bool] = False
    status: Optional[str] = "active"

class DocumentTypeUpdateSchema(BaseModel):
    document_name: Optional[str] = None
    description: Optional[str] = None
    is_mandatory: Optional[bool] = None
    status: Optional[str] = None
