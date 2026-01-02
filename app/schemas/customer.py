from pydantic import BaseModel, EmailStr
from typing import Optional

# for customer creation and update
class CustomerCreate(BaseModel):
    name: str
    contact_no: str
    email: EmailStr
    address: Optional[str] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None

# For returning customer data
class CustomerResponse(CustomerCreate):
    customer_id: int

    class Config:
        from_attributes = True