from fastapi import FastAPI, HTTPException
from app.database import engine, Base
from app.models import package, destination, customer, booking, payment
from app.routes import customer, package, destination, booking, payment

app = FastAPI(title="Travel Agency Management System")

Base.metadata.create_all(bind=engine)

app.include_router(customer.router)
app.include_router(package.router)
app.include_router(booking.router)
app.incude_router(payment.router)
app.include_router(destination.router)



