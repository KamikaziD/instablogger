import datetime
from fastapi import status, HTTPException
from routes.schemas import CommentCreate, Comment
from sqlalchemy.orm.session import Session
from db.models import DbUser, DbComments


def create_comment(db: Session, request: CommentCreate, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {request.username} doesn't exist"
        )
    new_comment = DbComments(
        username=username,
        text=request.comment,
        post_id=request.post_id,
        timestamp=datetime.datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all_comments(db: Session, post_id: int):
    return db.query(DbComments).filter(DbComments.post_id == post_id).all()
