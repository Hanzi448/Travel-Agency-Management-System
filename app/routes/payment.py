from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends
from app.exceptions import NotFoundError, ValidationError, ConflictError

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
    try:
        return create_payment(db, payment)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=list[PaymentResponse])
def read_payments(db: Session = Depends(get_db)):
    return get_all_payments(db)

@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        return get_payment_by_id(db, payment_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{payment_id}", response_model=PaymentResponse)
def edit_payment(payment_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
    try:
        return update_payment(db, payment_id, payment)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{payment_id}")
def remove_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        delete_payment(db, payment_id)
        return {"message": "Payment deleted successfully"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))