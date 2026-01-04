from sqlalchemy import Column, Integer, String, Text, Index
from app.database import Base

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_no = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    address = Column(Text)
    gender = Column(String(10))
    nationality = Column(String(50))

    __table_args__ = (
        Index("idx_customer_email", "email"),
    )
    
