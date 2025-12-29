from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.customer import CustomerCreate, CustomerResponse
from crud.customer import (
    create_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer,
    delete_customer,
)

router = APIRouter(prefix="/customers", tags=["customers"])

