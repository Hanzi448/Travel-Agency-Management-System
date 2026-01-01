from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends

from app.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.crud.booking import (
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    update_booking,
    delete_booking,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse)
def add_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    created = create_booking(db, booking)
    if not created:
        raise HTTPException(status_code=400, detail="Booking creation failed")
    return created

@router.get("/", response_model=list[BookingResponse])
def read_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)

@router.get("/{booking_id}", response_model=BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}", response_model=BookingResponse)
def edit_booking(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
    updated = update_booking(db, booking_id, booking)
    if not updated:
        raise HTTPException(status_code=404, detail="Booking not found or invalid customer_id/package_id")
    return updated

@router.delete("/{booking_id}")
def remove_booking(booking_id: int, db: Session = Depends(get_db)):
    deleted = delete_booking(db, booking_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted successfully"}