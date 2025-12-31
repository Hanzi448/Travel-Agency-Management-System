from sqlalchemy.orm import Session, func
from models.package import Package
from models.booking import Booking
from models.payment import Payment
from models.destination import Destination
from models.customer import Customer

def packages_by_destination(db: Session, destination_id: int):
    return db.query(Package).filter(Package.destination_id == destination_id).all()

def bookings_by_customer(db: Session, customer_id: int):
    return db.query(Booking).filter(Booking.customer_id == customer_id).all()

def total_revenue(db: Session):
    return db.query(func.sum(Payment.amount)).filter(Payment.payment_status == "Paid").scalar()

def most_popular_destinations(db: Session):
    return db.query(
        Destination.name,
        func.count(Booking.booking_id).label("total_bookings")
    ).join(Package, Package.destination_id == Destination.destination_id
    ).join(Booking, Booking.package_id == Package.package_id
    ).group_by(Destination.name
    ).order_by(func.count(Booking.booking_id).desc()
    ).all()

def pending_payments(db: Session):
    return db.query(
        Payment.payment_id,
        Payment.amount,
        Payment.payment_date,
        Customer.name.label("customer_name")
    ).join(Booking, Booking.booking_id == Payment.booking_id
    ).join(Customer, Customer.customer_id == Booking.customer_id
    ).filter(Payment.payment_status == "Unpaid"
    ).all()

