from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers.users import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)
from ..schemas.users import usersSchema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=usersSchema)
def create_new_user(request: usersSchema, db: Session = Depends(get_db)):
    return create_user(db, request)

@router.get("/", response_model=list[usersSchema])
def read_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get("/{user_id}", response_model=usersSchema)
def read_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=usersSchema)
def update_existing_user(user_id: str, request: usersSchema, db: Session = Depends(get_db)):
    user = update_user(db, user_id, request)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=usersSchema)
def delete_existing_user(user_id: str, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user