from pydantic import BaseModel
from typing import Optional

class BoardCreateSchema(BaseModel):
    board_name: str
    short_name: Optional[str] = None
    type: Optional[str] = None
    country: Optional[str] = "India"
    status: Optional[str] = "active"

class BoardUpdateSchema(BaseModel):
    board_name: Optional[str] = None
    short_name: Optional[str] = None
    type: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = None
