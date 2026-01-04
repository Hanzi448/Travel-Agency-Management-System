from sqlalchemy import Column, Integer, String, Text, Numeric, CheckConstraint, UniqueConstraint
from app.database import Base

class Destination(Base):
    __tablename__ = "destination"

    destination_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    description = Column(Text)
    average_cost = Column(Numeric(10, 2), CheckConstraint('average_cost >= 0'))

    __table_args__ = (
        UniqueConstraint("name", "country", name="uq_destination_name_country"),
    )