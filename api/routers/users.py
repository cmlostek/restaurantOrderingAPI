from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.schemas.review import Review
from api.controllers.review import (
    get_all_reviews_by_user,
    get_review_by_id,
    create_review,
    update_review,
    delete_review
)
from api.dependencies.database import get_db

from api.controllers.order_details import get_all_order_details, get_order_detail_by_id, update_order_detail
from api.schemas.order_details import OrderDetail


from ..schemas.order_details import OrderDetail
from api.dependencies.database import get_db

router = APIRouter(
    prefix="/users",tags=["users"]
)
@router.get("/", response_model=List[User])
def get_all_users(user_id: int,db: Session = Depends(get_db)):
    user_details = get_all_order_details(db, user_id)
    if not user_details:
        raise HTTPException(status_code=404,detail="No users found for your ID")
    return user_details

@router.get("/{user_id}", response_model=User)
def get_user_detail(user_id: int, detail_id: int, db: Session = Depends(get_db)):
    user_detail = get_user_by_id(db, user_id, detail_id)
    if not user_detail:
        raise HTTPException(status_code=404, detail=f"User with ID {detail_id} not found for user {user_id}")
    return user_detail

@router.post("/", response_model=User)
def create_user_detail(request: User, user_id: int, db: Session = Depends(get_db)):
    return create_user(request, user_id, db)

@router.put("/{detail_id}", response_model=User)
def update_user_detail(user_id: int, detail_id: int, request: User, db: Session = Depends(get_db)):
    user_detail = update_user(db, user_id, detail_id, request)
    if not user_detail:
        raise HTTPException(status_code=404, detail=f"User with ID {detail_id} not found for user {user_id}")
    return user_detail

@router.delete("/{detail_id}")
def delete_user_detail(user_id: int, detail_id: int, db: Session = Depends(get_db)):
    result = delete_user(db, user_id, detail_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"User with ID {detail_id} not found for user {user_id}")
    return {"detail": "User deleted successfully"}