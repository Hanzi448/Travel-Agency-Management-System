from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, CheckConstraint, Index
from app.database import Base

class Package(Base):
    __tablename__ = "package"

    package_id = Column(Integer, primary_key=True)
    destination_id = Column(
        Integer,
        ForeignKey("destination.destination_id", ondelete="CASCADE"),
        nullable=False
    )
    title = Column(String(150), nullable=False)
    duration = Column(Integer, CheckConstraint('duration > 0'), nullable=False)  # duration in days
    price = Column(Numeric(10, 2), CheckConstraint('price >= 0'))
    package_type = Column(String(50))

    __table_args__ = (
        Index("idx_package_destination", "destination_id"),
    )




    
