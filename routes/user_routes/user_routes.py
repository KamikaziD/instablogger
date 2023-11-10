from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from typing import List
from routes.schemas import UserDisplay, UserBase, UserAuth
from auth.oauth2 import get_current_user
from db.database import get_db
from db import db_user

router = APIRouter(prefix='/user', tags=['Users'])


@router.post("/", response_model=UserDisplay, description="Create a new user")
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.get("/", response_model=List[UserDisplay], description="Get all users")
def get_all_users(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.get_all_users(db)


@router.get("/{user_id}", response_model=UserDisplay, description="Get user by id")
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.get_user(user_id, db)


@router.delete("/{user_id}", description="Delete user by id")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    return db_user.delete_user(user_id, db)
