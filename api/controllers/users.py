from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.users import  User as model # SQLAlchemy User model
from ..schemas.users import usersSchema as User# Pydantic schema
from ..models.payment import Payment as payments # SQLAlchemy Payment model


def create_user(db: Session, request: User):

    new_user = model(
        user_id=request.user_id,
        # payment_id=payment_object.payment_id,
        user_name=request.user_name,
        email=request.email,
        phone_number=request.phone_number,
        address=request.address,
        user_role=request.user_role,
        payment_info=request.payment_info,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        print("here", e)
        error = str(e.__dict__['orig'])
        print("here", error)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_user


def get_all_users(db: Session):
        try:
            result = db.query(model).all()
            return result
        except SQLAlchemyError as e:
            error = str(e.__dict__.get('orig', 'Unknown error'))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_user_by_id(db: Session, user_id: int):
    try:
        user = db.query(model).filter(model.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return user


def update_user(db: Session, user_id: int, request: User):
    try:
        user = db.query(model).filter(model.user_id == user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        update_data = request.dict(exclude_unset=True)
        user.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return user.first()


def delete_user(db: Session, user_id: int):
    try:
        user = db.query(model).filter(model.user_id == user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return True