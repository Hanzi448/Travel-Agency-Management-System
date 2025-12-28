from pydantic import BaseModel, Field
from typing import Optional

class DestinationCreate(BaseModel):
    name: str
    country: str
    description: Optional[str] = None
    average_cost: float = Field(gt=0)

class DestinationResponse(DestinationCreate):
    destination_id: int

    class Config:
        from_attributes = True