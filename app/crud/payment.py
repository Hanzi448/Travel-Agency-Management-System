from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate

def create_payment(db: Session, payment: PaymentCreate):
    # FK validation: booking must exist
    booking = db.query(Booking).filter(
        Booking.booking_id == payment.booking_id
    ).first()

    if not booking:
        return None
    
    # Check if payment already exists (1-to-1)
    existing_payment = db.query(Payment).filter(
        Payment.booking_id == payment.booking_id
    ).first()
    if existing_payment:
        return None
    
    # Validate amount
    if payment.amount > booking.total_cost:
        return None

    db_payment = Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_all_payments(db: Session):
    return db.query(Payment).all()

def get_payment_by_id(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.payment_id == payment_id).first()

def update_payment(db: Session, payment_id: int, payment_data: PaymentCreate):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        return None
    
    booking = db.query(Booking).filter(
        Booking.booking_id == payment_data.booking_id
    ).first()

    if not booking:
        return None
    
    if payment_data.amount != booking.total_cost:
        return None
    
    for key, value in payment_data.model_dump().items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment

def delete_payment(db: Session, payment_id: int):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        return None

    db.delete(payment)
    db.commit()
    return payment






