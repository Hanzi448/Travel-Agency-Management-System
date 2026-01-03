from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.package import Package
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.destination import Destination
from app.models.customer import Customer
from app.exceptions import NotFoundError, ConflictError, ValidationError

def packages_by_destination(db: Session, destination_id: int):
    destination = db.query(Destination).filter(Destination.destination_id == destination_id).first()
    if not destination:
        raise NotFoundError(f"Destination with id {destination_id} not found.")
    
    package = db.query(Package).filter(Package.destination_id == destination_id).all()
    if not package:
        raise NotFoundError(f"No packages found for destination id {destination_id}.")
    
    return package

def bookings_by_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise NotFoundError(f"Customer with id {customer_id} not found.")
    
    bookings = db.query(Booking).filter(Booking.customer_id == customer_id).all()
    if not bookings:
        raise NotFoundError(f"No bookings found for customer id {customer_id}.")
    
    return bookings

def total_revenue(db: Session):
    revenue = db.query(func.sum(Payment.amount)).filter(Payment.payment_status == "Paid").scalar()

    if revenue is None:
        return NotFoundError("No paid payments found.")
    
    return revenue

def most_popular_destinations(db: Session):
    results = db.query(
        Destination.name.label("destination"),
        func.count(Booking.booking_id).label("total_bookings")
    ).join(
        Package, Package.destination_id == Destination.destination_id
    ).join(
        Booking, Booking.package_id == Package.package_id
    ).group_by(
        Destination.name
    ).order_by(
        func.count(Booking.booking_id).desc()
    ).all()

    if not results:
        raise NotFoundError("No booking data available to determine popular destinations.")

    return [
        {
            "destination": row.destination,
            "total_bookings": row.total_bookings
        }
        for row in results
    ]


def pending_payments(db: Session):
    payments =  db.query(
        Payment.payment_id,
        Payment.amount,
        Payment.payment_date,
        Customer.name.label("customer_name")
    ).join(Booking, Booking.booking_id == Payment.booking_id
    ).join(Customer, Customer.customer_id == Booking.customer_id
    ).filter(Payment.payment_status == "Unpaid"
    ).all()

    if not payments:
        raise NotFoundError("No pending payments found.")
    
    return payments