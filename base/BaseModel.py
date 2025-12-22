from typing import Optional
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id: Optional[int] = None
        self.is_deleted: bool = False
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()
    
    def to_dict(self):
        return {
            "id": self.id,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
