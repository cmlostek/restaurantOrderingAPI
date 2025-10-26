from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

from ..models.users import  User as model 
from ..schemas.users import usersCreate as User
from ..models.payment import Payment as payments 

def hash_password(password: str) -> str:
    """Hash a password using bcrypt directly"""
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def create_user(db: Session, request: User):

    new_user = model(
        username=request.username,
        password=hash_password(request.password),
        email=request.email,
        phone_number=request.phone_number,
        address=request.address,
        user_role=request.user_role,
        payment_info=request.payment_info,
        review=request.review,
        rating=request.rating
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


def get_user_by_username(db: Session, username: str):
    """Get user by username for authentication"""
    try:
        user = db.query(model).filter(model.username == username).first()
        return user
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', 'Unknown error'))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return user


def verify_user_credentials(db: Session, username: str, password: str):
    """Verify username and password credentials"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    return verify_password(password, user.password)


def update_user(db: Session, user_id: int, request: User):
    try:
        user = db.query(model).filter(model.user_id == user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Hash password if it's being updated
        update_data = request.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['password'] = hash_password(update_data['password'])
        
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
