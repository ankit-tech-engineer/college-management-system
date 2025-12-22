from pydantic import BaseModel
from typing import Optional

class CityModel(BaseModel):
    name: str
    state_id: str

class CityUpdateModel(BaseModel):
    name: Optional[str] = None
    state_id: Optional[str] = None
