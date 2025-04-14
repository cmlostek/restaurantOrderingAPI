from sqlalchemy.orm import Session
from ..models.users import users
from ..schemas.users import usersSchema

def create_user(db: Session, request: usersSchema):
    new_user = users(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(users).all()

def get_user_by_id(db: Session, user_id: str):
    return db.query(users).filter(users.user_id == user_id).first()

def update_user(db: Session, user_id: str, request: usersSchema):
    user = db.query(users).filter(users.user_id == user_id).first()
    if user:
        for key, value in request.dict().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: str):
    user = db.query(users).filter(users.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user