from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    model_config = ConfigDict()

    id: int
    username: str
    email: str
    created_date: datetime


class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int


class PostCreate(BaseModel):
    image_url: str
    image_url_type: str
    caption: str


# for PostDisplay
class User(BaseModel):
    """User display for the PostDisplay"""
    model_config = ConfigDict()
    username: str


# for CommentDisplay
class Comment(BaseModel):
    text: str
    username: str
    timestamp: datetime


class UserAuth(BaseModel):
    id: int
    username: str
    email: str


class PostDisplay(BaseModel):
    model_config = ConfigDict()
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: User
    comments: List[Comment]


class CommentCreate(BaseModel):
    comment: str
    post_id: int
