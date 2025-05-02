from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers.payment import (
    create_payment,
    get_all_payments,
    get_payment_by_id,
    update_payment,
    delete_payment,
)
from ..schemas.payment import PaymentCreate, PaymentSchema, PaymentUpdate
from ..dependencies.database import get_db

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/", response_model=list[PaymentSchema])
def read_all_payments(db: Session = Depends(get_db)):
    payments = get_all_payments(db)
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found")
    return payments

@router.post("/", response_model=PaymentSchema)
def create_new_payment(request: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment(db, request)

@router.get("/{payment_id}", response_model=PaymentSchema)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    obj = get_payment_by_id(db, payment_id)
    if not obj:
        raise HTTPException(404, "Payment not found")
    return obj

@router.put("/{payment_id}", response_model=PaymentSchema)
def update_existing_payment(payment_id: int, request: PaymentUpdate, db: Session = Depends(get_db)):
    obj = update_payment(db, payment_id, request)
    if not obj:
        raise HTTPException(404, "Payment not found")
    return obj

@router.delete("/{payment_id}", response_model=PaymentSchema)
def delete_existing_payment(payment_id: int, db: Session = Depends(get_db)):
    obj = delete_payment(db, payment_id)
    if not obj:
        raise HTTPException(404, "Payment not found")
    return obj
