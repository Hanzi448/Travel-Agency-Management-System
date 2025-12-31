from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends

from database import get_db
from schemas.destination import DestinationCreate, DestinationResponse
from crud.destination import (
    create_destination,
    get_all_destinations,
    get_destination_by_id,
    update_destination,
    delete_destination,
)

router = APIRouter(prefix="/destinations", tags=["destinations"])

@router.post("/", response_model=DestinationResponse)
def add_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    created = create_destination(db, destination)
    if not created:
        raise HTTPException(status_code=400, detail="Destination creation failed")
    return created

@router.get("/", response_model=list[DestinationResponse])
def read_destinations(db: Session = Depends(get_db)):
    return get_all_destinations(db)

@router.get("/{destination_id}", response_model=DestinationResponse)
def read_destination(destination_id: int, db: Session = Depends(get_db)):
    destination = get_destination_by_id(db, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination

@router.put("/{destination_id}", response_model=DestinationResponse)
def edit_destination(destination_id: int, destination: DestinationCreate, db: Session = Depends(get_db)):
    updated = update_destination(db, destination_id, destination)
    if not updated:
        raise HTTPException(status_code=404, detail="Destination not found")
    return updated

@router.delete("/{destination_id}")
def remove_destination(destination_id: int, db: Session = Depends(get_db)):
    deleted = delete_destination(db, destination_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Destination not found")
    return {"message": "Destination deleted successfully"}

