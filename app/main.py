from fastapi import FastAPI, HTTPException
from database import engine, Base
from models import package, destination, customer, booking, payment

app = FastAPI(title="Travel Agency Management System")

Base.metadata.create_all(bind=engine)