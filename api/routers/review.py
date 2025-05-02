from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.schemas.review import Review
from api.controllers.review import (
    read_all   as get_all_reviews_by_user,
    read_one   as get_review_by_id,
    create     as create_review,
    update     as update_review,
    delete     as delete_review,
)
from api.dependencies.database import get_db

router = APIRouter(
    prefix="/reviews", tags=["reviews"]
)

@router.get("/", response_model=List[Review])
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = get_all_reviews_by_user(db)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    return reviews


@router.get("/{review_id}", response_model=Review)
def get_review(user_id: int, review_id: int, db: Session = Depends(get_db)):
    review = get_review_by_id(db, user_id, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review with ID not found")
    return review

@router.post("/", response_model=Review)
def create_review_entry(request: Review, user_id: int, db: Session = Depends(get_db)):
    return create_review(db, request, user_id)

@router.put("/{review_id}", response_model=Review)
def update_review_entry(user_id: int, review_id: int, request: Review, db: Session = Depends(get_db)):
    updated_review = update_review(db, user_id, review_id, request)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@router.delete("/{review_id}")
def delete_review_entry(user_id: int, review_id: int, db: Session = Depends(get_db)):
    result = delete_review(db, user_id, review_id)
    if not result:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"detail": "Review deleted successfully"}

@router.delete("/")
def delete_all_reviews(user_id: int, db: Session = Depends(get_db)):
    reviews = get_all_reviews_by_user(db)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    for review in reviews:
        delete_review(db, user_id, review.review_id)
    return {"detail": "All reviews deleted successfully"}