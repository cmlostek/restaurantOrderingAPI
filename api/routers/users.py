from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.controllers.order_details import update_order_detail
from api.controllers.users import get_all_users, get_user_by_id, create_user, update_user, delete_user, verify_user_credentials, get_user_by_username

from ..schemas.users import usersCreate as usersSchema
from ..schemas.users import usersResponse, usersLogin
from api.dependencies.database import get_db

router = APIRouter(
    prefix="/users", tags=["users"]
)

@router.get("/", response_model=list[usersResponse])
def read_all_users(db: Session = Depends(get_db)):
    user_details = get_all_users(db)
    if not user_details:
        raise HTTPException(status_code=404, detail="No users found")
    return user_details

@router.get("/{user_id}", response_model=usersResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_detail = get_user_by_id(db, user_id)
    if not user_detail:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user_detail

@router.post("/", response_model=usersResponse)
def create_new_user(request: usersSchema, db: Session = Depends(get_db)):
    return create_user(db, request)

@router.put("/{user_id}", response_model=usersResponse)
def update_existing_user(user_id: int, request: usersSchema, db: Session = Depends(get_db)):
    user_detail = update_user(db, user_id, request)
    if not user_detail:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user_detail

@router.delete("/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    result = delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return {"detail": "User deleted successfully"}

@router.post("/login", response_model=usersResponse)
def login_user(credentials: usersLogin, db: Session = Depends(get_db)):
    """Login endpoint to authenticate user with username and password"""
    user = get_user_by_username(db, credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if verify_user_credentials(db, credentials.username, credentials.password):
        return user
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")