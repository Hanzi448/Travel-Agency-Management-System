from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends
from app.exceptions import NotFoundError

from app.database import get_db
from app.schemas.destination import DestinationCreate, DestinationResponse
from app.services.destination import (
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
    try:
        return get_destination_by_id(db, destination_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{destination_id}", response_model=DestinationResponse)
def edit_destination(destination_id: int, destination: DestinationCreate, db: Session = Depends(get_db)):
    try:
        return update_destination(db, destination_id, destination)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{destination_id}")
def remove_destination(destination_id: int, db: Session = Depends(get_db)):
    try:
        delete_destination(db, destination_id)
        return {"message" : "Destination deleted successfully"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

