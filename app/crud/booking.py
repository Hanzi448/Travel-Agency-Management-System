from sqlalchemy.orm import Session
from models.booking import Booking
from models.customer import Customer
from models.package import Package
from schemas.booking import BookingCreate

def create_booking(db: Session, booking: BookingCreate):
    # Validate that customer exists
    customer = db.query(Customer).filter(
        Customer.customer_id == booking.customer_id
    ).first()
    if not customer:
        return None
    
    # Validate that package exists
    package = db.query(Package).filter(
        Package.package_id == booking.package_id
    ).first()
    if not package:
        return None
    
    # Calculate total cost (DERIVED ATTRIBUTE)
    total_cost = package.price * booking.no_of_persons

    db_booking = Booking(
        customer_id=booking.customer_id,
        package_id=booking.package_id,
        booking_date=booking.booking_date,
        no_of_persons=booking.no_of_persons,
        total_cost=total_cost,
        status = booking.status
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking, None

def get_all_bookings(db: Session):
    return db.query(Booking).all()

def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.booking_id == booking_id).first()

def update_booking(db: Session, booking_id: int, booking_data: BookingCreate):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return None, "Booking not found"

    # Validate that customer exists
    customer = db.query(Customer).filter(
        Customer.customer_id == booking_data.customer_id
    ).first()
    if not customer:
        return None, "Customer not found"
    
    # Validate that package exists
    package = db.query(Package).filter(
        Package.package_id == booking_data.package_id
    ).first()
    if not package:
        return None, "Package not found"

    booking.customer_id = booking_data.customer_id
    booking.package_id = booking_data.package_id
    booking.booking_date = booking_data.booking_date
    booking.no_of_persons = booking_data.no_of_persons
    booking.status = booking_data.status

    # Recalculate total cost
    booking.total_cost = package.price * booking_data.no_of_persons

    db.commit()
    db.refresh(booking)
    return booking, None

def delete_booking(db: Session, booking_id: int):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return None

    db.delete(booking)
    db.commit()
    return booking



