from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers.promotion import (
    create_promotion,
    get_promotion_by_id,
    update_promotion,
    delete_promotion,
)
from ..schemas.promotion import PromotionCreate, PromotionSchema, PromotionUpdate
from ..dependencies.database import get_db

router = APIRouter(prefix="/promotions", tags=["promotions"])

@router.post("/", response_model=PromotionSchema)
def create_new_promotion(request: PromotionCreate, db: Session = Depends(get_db)):
    return create_promotion(db, request)

@router.get("/{promotion_id}", response_model=PromotionSchema)
def read_promotion(promotion_id: int, db: Session = Depends(get_db)):
    obj = get_promotion_by_id(db, promotion_id)
    if not obj:
        raise HTTPException(404, "Promotion not found")
    return obj

@router.put("/{promotion_id}", response_model=PromotionSchema)
def update_existing_promotion(promotion_id: int, request: PromotionUpdate, db: Session = Depends(get_db)):
    obj = update_promotion(db, promotion_id, request)
    if not obj:
        raise HTTPException(404, "Promotion not found")
    return obj

@router.delete("/{promotion_id}", response_model=PromotionSchema)
def delete_existing_promotion(promotion_id: int, db: Session = Depends(get_db)):
    obj = delete_promotion(db, promotion_id)
    if not obj:
        raise HTTPException(404, "Promotion not found")
    return obj
