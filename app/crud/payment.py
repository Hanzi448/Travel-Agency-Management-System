from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate
from app.exceptions import NotFoundError, ValidationError, ConflictError

def create_payment(db: Session, payment: PaymentCreate):
    # FK validation: booking must exist
    booking = db.query(Booking).filter(
        Booking.booking_id == payment.booking_id
    ).first()

    if not booking:
        raise NotFoundError(f"Booking with id {payment.booking_id} not found.")
    
    # Check if payment already exists (1-to-1)
    existing_payment = db.query(Payment).filter(
        Payment.booking_id == payment.booking_id
    ).first()
    if existing_payment:
        raise ConflictError("Payment already paid.")
    
    # Validate amount
    if payment.amount != booking.total_cost:
        raise ValidationError("Invalid amount!")

    db_payment = Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_all_payments(db: Session):
    return db.query(Payment).all()

def get_payment_by_id(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise NotFoundError(f"Payment with od {payment_id} not found.")

def update_payment(db: Session, payment_id: int, payment_data: PaymentCreate):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        raise NotFoundError(f"Payment with od {payment_id} not found.")
    
    booking = db.query(Booking).filter(
        Booking.booking_id == payment_data.booking_id
    ).first()

    if not booking:
        raise NotFoundError(f"Booking with id {payment_data.booking_id} not found")
    
    if payment_data.amount != booking.total_cost:
        raise ValidationError("Invalid amount!")
    
    for key, value in payment_data.model_dump().items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment

def delete_payment(db: Session, payment_id: int):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        raise NotFoundError(f"Payment with od {payment_id} not found.")

    db.delete(payment)
    db.commit()
    return payment






