from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    id: Optional[int] = None
    is_deleted: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True

class CreateSchema(BaseModel):
    pass

class UpdateSchema(BaseModel):
    pass
