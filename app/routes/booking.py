from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends
from app.exceptions import NotFoundError

from app.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking import (
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    update_booking,
    delete_booking,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse)
def add_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        return create_booking(db, booking)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[BookingResponse])
def read_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)

@router.get("/{booking_id}", response_model=BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        return get_booking_by_id(db, booking_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{booking_id}", response_model=BookingResponse)
def edit_booking(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        return update_booking(db, booking_id, booking)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{booking_id}")
def remove_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        delete_booking(db, booking_id)
        return {"message": "Booking deleted successfully"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str)