from pydantic import BaseModel
from typing import Optional

class FeeTypeCreateSchema(BaseModel):
    fee_type_name: str
    description: Optional[str] = None
    status: Optional[str] = "active"

class FeeTypeUpdateSchema(BaseModel):
    fee_type_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
