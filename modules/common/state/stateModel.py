from pydantic import BaseModel
from typing import Optional

class StateModel(BaseModel):
    name: str
    code: str
    country_id: str

class StateUpdateModel(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    country_id: Optional[str] = None
