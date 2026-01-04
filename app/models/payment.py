from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey, CheckConstraint, UniqueConstraint
from app.database import Base

class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(
        Integer,
        ForeignKey("booking.booking_id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    amount = Column(Numeric(10, 2), CheckConstraint('amount > 0'))
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50))
    payment_status = Column(String(30), default="Unpaid")
    
    __table_args__ = (
        UniqueConstraint("booking_id", name="uq_payment_booking"),
    )