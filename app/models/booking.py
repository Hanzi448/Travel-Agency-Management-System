from sqlalchemy import Column, Integer, ForeignKey, Date, CheckConstraint, String, Numeric
from app.database import Base

class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer, 
        ForeignKey("customer.customer_id", ondelete="CASCADE"),
        nullable=False
    )
    package_id = Column(
        Integer,
        ForeignKey("package.package_id", ondelete="CASCADE"),
        nullable=False
    )
    booking_date = Column(Date, nullable=False)
    no_of_persons = Column(Integer, CheckConstraint('no_of_persons > 0'))
    total_cost = Column(Numeric(10, 2), CheckConstraint('total_cost > 0'))
    status = Column(String(30), default="Pending")

