import datetime
from fastapi import status, HTTPException
from routes.schemas import PostCreate
from sqlalchemy.orm.session import Session
from db.models import DbPosts, DbUser


def create_post(db: Session, request: PostCreate, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {request.creator_id} doesn't exist"
        )
    new_post = DbPosts(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        user_id=user_id,
        timestamp=datetime.datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all_posts(db: Session):
    return db.query(DbPosts).all()


def get_post(post_id: int, db: Session):
    post = db.query(DbPosts).filter(DbPosts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


def delete_post(post_id: int, db: Session, user_id: int):
    post = db.query(DbPosts).filter(DbPosts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator of the post can delete this post")

    db.delete(post)
    db.commit()
    return {'success': f'Post {id} deleted'}
