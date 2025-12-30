from sqlalchemy.orm import Session
from models.package import Package
from models.destination import Destination
from schemas.package import PackageCreate


def create_package(db: Session, package: PackageCreate):
    # FK validation: destination must exist
    destination = db.query(Destination).filter(
        Destination.destination_id == package.destination_id
    ).first()

    if not destination:
        return None

    db_package = Package(**package.model_dump())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

def get_all_packages(db: Session):
    return db.query(Package).all()

def get_package_by_id(db: Session, package_id: int):
    return db.query(Package).filter(Package.package_id == package_id).first()

def update_package(db: Session, package_id: int, package_data: PackageCreate):
    package = get_package_by_id(db, package_id)
    if not package:
        return None

    # FK validation: destination must exist
    destination = db.query(Destination).filter(
        Destination.destination_id == package_data.destination_id
    ).first()

    if not destination:
        return None

    for key, value in package_data.model_dump().items():
        setattr(package, key, value)

    db.commit()
    db.refresh(package)
    return package

def delete_package(db: Session, package_id: int):
    package = get_package_by_id(db, package_id)
    if not package:
        return None

    db.delete(package)
    db.commit()
    return package



