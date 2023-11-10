from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm.session import Session
from typing import List
from routes.schemas import CommentCreate, Comment, UserAuth
from db.database import get_db
from auth.oauth2 import get_current_user
from db import db_comment

router = APIRouter(prefix='/comment', tags=['Comments'])


@router.post("/",
             response_model=Comment,
             description="Create a new comment for the user that is logged in.")
def create_comment(
        request: CommentCreate,
        db: Session = Depends(get_db),
        current_user: UserAuth = Depends(get_current_user)
):
    return db_comment.create_comment(db, request, current_user.username)


@router.get("/{post_id}", response_model=List[Comment], description="Get all comments for the relevant post_id")
def get_all_comments(post_id: int, db: Session = Depends(get_db)):
    return db_comment.get_all_comments(db, post_id)
