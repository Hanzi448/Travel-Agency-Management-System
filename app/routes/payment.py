from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends

from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.crud.payment import (
    create_payment,
    get_all_payments,
    get_payment_by_id,
    update_payment,
    delete_payment,
)

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse)
def add_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    created = create_payment(db, payment)
    if not created:
        raise HTTPException(status_code=400, detail="Invalid booking, duplicate payment, or invalid amount")
    return created

@router.get("/", response_model=list[PaymentResponse])
def read_payments(db: Session = Depends(get_db)):
    return get_all_payments(db)

@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/{payment_id}", response_model=PaymentResponse)
def edit_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
    updated = update_payment(db, payment_id, payment)
    if not updated:
        raise HTTPException(status_code=404, detail="Invalid booking, duplicate payment, or invalid amount")
    return updated

@router.delete("/{payment_id}")
def remove_payment(payment_id: int, db: Session = Depends(get_db)):
    deleted = delete_payment(db, payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}