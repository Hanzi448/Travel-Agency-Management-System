from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PaymentCreate(BaseModel):
    booking_id: int
    amount: float = Field(gt=0)
    payment_date: date  # ISO format date string
    payment_method: Optional[str] = None
    status: Optional[str] = "Unpaid"

class PaymentResponse(PaymentCreate):
    payment_id: int

    class Config:
        from_attributes = True
