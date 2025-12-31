from sqlalchemy.orm import Session
from models.destination import Destination
from app.schemas.destination import DestinationCreate

def create_destination(db: Session, destination: DestinationCreate):
    db_destination = Destination(**destination.model_dump())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

def get_all_destinations(db: Session):
    return db.query(Destination).all()

def get_destination_by_id(db: Session, destination_id: int):
    return db.query(Destination).filter(Destination.id == destination_id).first()

def update_destination(db: Session, destination_id: int, destination_data: DestinationCreate):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        return None
    
    for key, value in destination_data.model_dump().items():
        setattr(destination, key, value)
    
    db.commit()
    db.refresh(destination)
    return destination

def delete_destination(db: Session, destination_id: int):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        return None
    
    db.delete(destination)
    db.commit()
    return destination



