from sqlalchemy.orm import Session
from models.booking import Booking
from models.payment import Payment
from schemas.payment import PaymentCreate

def create_payment(db: Session, payment: PaymentCreate):
    # FK validation: booking must exist
    booking = db.query(Booking).filter(
        Booking.booking_id == payment.booking_id
    ).first()

    if not booking:
        return None, "Booking not found"
    
    # Check if payment already exists (1-to-1)
    existing_payment = db.query(Payment).filter(
        Payment.booking_id == payment.booking_id
    ).first()
    if existing_payment:
        return None, "Payment for this booking already exists"
    
    # Validate amount
    if payment.amount > booking.total_price:
        return None, "Payment amount exceeds booking total price"

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
        return None, "Payment not found"
    
    booking = db.query(Booking).filter(
        Booking.booking_id == payment_data.booking_id
    ).first()

    if not booking:
        return None, "Booking not found"
    
    if payment_data.amount > booking.total_price:
        return None, "Payment amount exceeds booking total price"
    
    for key, value in payment_data.model_dump().items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment, None

def delete_payment(db: Session, payment_id: int):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        return None, "Payment not found"

    db.delete(payment)
    db.commit()
    return payment






