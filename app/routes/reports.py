from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
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
def get_packages_by_destination(destination_id: int, db: Session = Depends(get_db)):
    try:
        return packages_by_destination(db, destination_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/bookings_by_customer/{customer_id}")
def get_bookings_by_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        return bookings_by_customer(db, customer_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/total_revenue")
def get_total_revenue(db: Session = Depends(get_db)):
    try:
        return {"total_revenue": total_revenue(db)}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/most_popular_destinations")
def get_most_popular_destinations(db: Session = Depends(get_db)):
    try:
        return most_popular_destinations(db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/pending_payments")
def get_pending_payments(db: Session = Depends(get_db)):
    try:
        return pending_payments(db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

