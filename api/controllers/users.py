from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.users import User
from ..schemas.users import usersSchema
from sqlalchemy.exc import SQLAlchemyError

import api.models.users as model  # SQLAlchemy User model
from api.schemas.users import usersSchema  # Pydantic schema

def create_user(db: Session, request: usersSchema):
    new_user = usersSchema(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

def create(db: Session, request: User):
    new_user = model.User(
        user_name=request.user_name,
        email=request.email,
        phone_number=request.phone_number,
        address=request.address,
        user_role=request.user_role,
        pay_info=request.payment_info,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_user

def get_all_users(db: Session):
    return db.query(usersSchema).all()

def get_user_by_id(db: Session, user_id: str):
    return db.query(usersSchema).filter(usersSchema.user_id == user_id).first()
def read_all(db: Session):
    try:
        result = db.query(model.User).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def update_user(db: Session, user_id: str, request: usersSchema):
    user = db.query(usersSchema).filter(usersSchema.user_id == user_id).first()
    if user:
        for key, value in request.dict().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)

def read_one(db: Session, user_id: int):
    try:
        user = db.query(model.User).filter(model.User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return user

def delete_user(db: Session, user_id: str):
    user = db.query(usersSchema).filter(usersSchema.user_id == user_id).first()
    if user:
        db.delete(user)

def update(db: Session, user_id: int, request: User):
    try:
        user = db.query(model.User).filter(model.User.user_id == user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        update_data = request.dict(exclude_unset=True)
        user.update(update_data, synchronize_session=False)
        db.commit()
           # return user
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return usersSchema.first()


def delete(db: Session, user_id: int):
    try:
        user = db.query(model.User).filter(model.User.user_id == user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return True