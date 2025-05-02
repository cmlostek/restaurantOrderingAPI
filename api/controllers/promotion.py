from sqlalchemy.orm import Session
from ..models.promotion import Promotion
from ..schemas.promotion import PromotionCreate, PromotionUpdate

def get_all_promotions(db: Session):
    return db.query(Promotion).all()

def create_promotion(db: Session, data: PromotionCreate) -> Promotion:
    obj = Promotion(**data.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def get_promotion_by_id(db: Session, promotion_id: int) -> Promotion:
    return db.query(Promotion).filter(Promotion.promotion_id == promotion_id).first()

def update_promotion(db: Session, promotion_id: int, data: PromotionUpdate) -> Promotion:
    obj = get_promotion_by_id(db, promotion_id)
    if not obj:
        return None
    for key, val in data.dict().items():
        setattr(obj, key, val)
    db.commit(); db.refresh(obj)
    return obj

def delete_promotion(db: Session, promotion_id: int) -> Promotion:
    obj = get_promotion_by_id(db, promotion_id)
    if not obj:
        return None
    db.delete(obj); db.commit()
    return obj
