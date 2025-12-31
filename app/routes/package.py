from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.package import PackageCreate, PackageResponse
from crud.package import (
    create_package,
    get_all_packaages,
    get_package_by_id,
    update_package,
    delete_package,
)

router = APIRouter(prefix="/packages", tags=["packages"])

@router.post("/", response_model=PackageResponse)
def add_package(package: PackageCreate, db: Session = Depends(get_db)):
    created = create_package(db, package)
    if not created:
        raise HTTPException(status_code=400, detail="Invalid destination_id")
    return created

@router.get("/", response_model=list[PackageResponse])
def read_packages(db: Session = Depends(get_db)):
    return get_all_packaages(db)

@router.get("/{package_id}", response_model=PackageResponse)
def read_package(package_id: int, db: Session = Depends(get_db)):
    package = get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

@router.put("/{package_id}", response_model=PackageResponse)
def edit_package(package_id: int, package: PackageCreate, db: Session = Depends(get_db)):
    updated = update_package(db, package_id, package)
    if not updated:
        raise HTTPException(status_code=404, detail="Package not found or invalid destination_id")
    return updated

@router.delete("/{package_id}")
def remove_package(package_id: int, db: Session = Depends(get_db)):
    deleted = delete_package(db, package_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"message": "Package deleted successfully"}