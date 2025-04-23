from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import api.models.review as model  # SQLAlchemy model for Review
from api.schemas.review import Review  # Pydantic schema


def create(db: Session, request: Review, user_id: int):
    new_review = model.Review(
        user_id=user_id,
        order_id=request.order_id,
        rating=request.rating,
        comment=request.comment,
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review


def read_all(db: Session, user_id: int):
    try:
        result = db.query(model.Review).filter(model.Review.user_id == user_id).all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found for this user")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result


def read_one(db: Session, user_id: int, review_id: int):
    try:
        review = db.query(model.Review).filter(
            model.Review.user_id == user_id,
            model.Review.review_id == review_id
        ).first()

        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return review


def update(db: Session, user_id: int, review_id: int, request: Review):
    try:
        review = db.query(model.Review).filter(
            model.Review.user_id == user_id,
            model.Review.review_id == review_id
        )

        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        update_data = request.dict(exclude_unset=True)
        review.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return review.first()


def delete(db: Session, user_id: int, review_id: int):
    try:
        review = db.query(model.Review).filter(
            model.Review.user_id == user_id,
            model.Review.review_id == review_id
        )

        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        review.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return True