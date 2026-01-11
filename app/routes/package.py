from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.exceptions import NotFoundError

from app.database import get_db
from app.schemas.package import PackageCreate, PackageResponse
from app.services.package import (
    create_package,
    get_all_packages,
    get_package_by_id,
    update_package,
    delete_package,
)

router = APIRouter(prefix="/packages", tags=["packages"])

@router.post("/", response_model=PackageResponse)
def add_package(package: PackageCreate, db: Session = Depends(get_db)):
    try:
        return create_package(db, package)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[PackageResponse])
def read_packages(db: Session = Depends(get_db)):
    return get_all_packages(db)

@router.get("/{package_id}", response_model=PackageResponse)
def read_package(package_id: int, db: Session = Depends(get_db)):
    try:
        return get_package_by_id(db, package_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{package_id}", response_model=PackageResponse)
def edit_package(package_id: int, package: PackageCreate, db: Session = Depends(get_db)):
    try:
        return update_package(db, package_id, package)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{package_id}")
def remove_package(package_id: int, db: Session = Depends(get_db)):
    try:
        delete_package(db, package_id)
        return {"message": "Package deleted successfully"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))