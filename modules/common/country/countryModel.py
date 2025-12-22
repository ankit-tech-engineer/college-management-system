from pydantic import BaseModel
from typing import Optional

class CountryModel(BaseModel):
    name: str
    code: str
    phone_code: Optional[str] = None

class CountryUpdateModel(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    phone_code: Optional[str] = None
