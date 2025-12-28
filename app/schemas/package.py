from pydantic import BaseModel, Field
from typing import Optional

class PackageCreate(BaseModel):
    destination_id: int
    title: str
    duration: int = Field(gt=0)
    price: float = Field(gt=0)
    package_type: Optional[str] = None


class PackageResponse(PackageCreate):
    package_id: int

    class Config:
        from_attributes = True
