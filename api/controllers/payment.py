from sqlalchemy.orm import Session
from ..models.payment import Payment
from ..schemas.payment import PaymentCreate, PaymentUpdate

def create_payment(db: Session, data: PaymentCreate) -> Payment:
    obj = Payment(**data.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def get_payment_by_id(db: Session, payment_id: int) -> Payment:
    return db.query(Payment).filter(Payment.payment_id == payment_id).first()

def update_payment(db: Session, payment_id: int, data: PaymentUpdate) -> Payment:
    obj = get_payment_by_id(db, payment_id)
    if not obj:
        return None
    for key, val in data.dict().items():
        setattr(obj, key, val)
    db.commit(); db.refresh(obj)
    return obj

def delete_payment(db: Session, payment_id: int) -> Payment:
    obj = get_payment_by_id(db, payment_id)
    if not obj:
        return None
    db.delete(obj); db.commit()
    return obj
