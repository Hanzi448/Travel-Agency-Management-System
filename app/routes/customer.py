from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.exceptions import NotFoundError
from app.services.customer import (
    create_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer,
    delete_customer,
)

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse)
def add_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    customer = create_customer(db, customer)
    if not customer:
        raise HTTPException(status_code=400, detail="Customer creation failed")
    return customer

@router.get("/", response_model=list[CustomerResponse])
def read_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        return get_customer_by_id(db, customer_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{customer_id}", response_model=CustomerResponse)
def edit_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        return update_customer(db, customer_id, customer)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{customer_id}")
def remove_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        delete_customer(db, customer_id)
        return {"message" : "Customer deleted successfully."}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

