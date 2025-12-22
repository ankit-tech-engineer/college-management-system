from pydantic import BaseModel

class UpdateApplicationStatusModel(BaseModel):
    application_status: str
