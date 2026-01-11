from sqlalchemy.orm import Session
from app.models.destination import Destination
from app.schemas.destination import DestinationCreate
from app.exceptions import NotFoundError

def create_destination(db: Session, destination: DestinationCreate):
    db_destination = Destination(**destination.model_dump())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

def get_all_destinations(db: Session):
    return db.query(Destination).all()

def get_destination_by_id(db: Session, destination_id: int):
    destination = db.query(Destination).filter(Destination.destination_id == destination_id).first()
    if not destination:
        raise NotFoundError(f"Destination with id {destination_id} not found.")
    return destination

def update_destination(db: Session, destination_id: int, destination_data: DestinationCreate):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise NotFoundError(f"Destination with id {destination_id} not found.")
    
    for key, value in destination_data.model_dump().items():
        setattr(destination, key, value)
    
    db.commit()
    db.refresh(destination)
    return destination

def delete_destination(db: Session, destination_id: int):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise NotFoundError(f"Destination with id {destination_id} not found.")
    
    db.delete(destination)
    db.commit()
    return destination



