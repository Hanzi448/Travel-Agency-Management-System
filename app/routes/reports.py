from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.reports.reports import (
    packages_by_destination,
    bookings_by_customer,
    total_revenue,
    most_popular_destinations,
    pending_payments,
)

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/packages_by_destination/{destination_id}")
def report_packages_by_destination(destination_id: int, db: Session = Depends(get_db)):
    return packages_by_destination(db, destination_id)

@router.get("/bookings_by_customer/{customer_id}")
def get_bookings_by_customer(customer_id: int, db: Session = Depends(get_db)):
    return bookings_by_customer(db, customer_id)

@router.get("/total_revenue")
def get_total_revenue(db: Session = Depends(get_db)):
    return {"total_revenue": total_revenue(db)}

@router.get("/most_popular_destinations")
def get_most_popular_destinations(db: Session = Depends(get_db)):
    return most_popular_destinations(db)

@router.get("/pending_payments")
def get_pending_payments(db: Session = Depends(get_db)):
    return pending_payments(db)

