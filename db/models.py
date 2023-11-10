import datetime
from db.database import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime


class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_date = Column(DateTime)
    items = relationship('DbPosts',  back_populates='user')


class DbPosts(Base):
    __tablename__ = "posts"
    id = Column(Integer, index=True, primary_key=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('DbUser', back_populates='items')
    comments = relationship('DbComments', back_populates='post')


class DbComments(Base):
    __tablename__ = "comments"
    id = Column(Integer, index=True, primary_key=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('DbPosts', back_populates="comments")
