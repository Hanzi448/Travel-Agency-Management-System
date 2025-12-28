from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookingCreate(BaseModel):
    customer_id: int
    package_id: int
    booking_date: date  # ISO format date string
    no_of_persons: int = Field(gt=0)
    status: Optional[str] = "Pending"

class BookingResponse(BookingCreate):
    booking_id: int
    total_cost: float

    class Config:
        from_attributes = True