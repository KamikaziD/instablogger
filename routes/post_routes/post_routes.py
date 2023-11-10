from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm.session import Session
from typing import List
from routes.schemas import PostCreate, PostDisplay, UserAuth
from db.database import get_db
from auth.oauth2 import get_current_user
from db import db_post
from utils.utils import format_file_size
import random
import string
import shutil

router = APIRouter(prefix='/post', tags=['Posts'])


@router.post("/",
             response_model=PostDisplay,
             description="""
             ## Create a new post for the user that is logged in.\n
*Auth Required \n
**IMAGE URL TYPES:**
- absolute = 'http://randomdomain.com/random_image.jpg'
- relative = 'images/my_uploaded_image.jpg' 
**Use the /post/image endpoint first for relative images upload*
""")
def create_post(
        request: PostCreate,
        db: Session = Depends(get_db),
        current_user: UserAuth = Depends(get_current_user)
):
    image_url_types = ['absolute', 'relative']
    if request.image_url_type not in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parameter image_url_type can only take values 'absolute' or 'relative'")
    return db_post.create_post(db, request, current_user.id)


@router.get("/", response_model=List[PostDisplay], description="Get all posts")
def get_all_posts(db: Session = Depends(get_db)):
    return db_post.get_all_posts(db)


@router.get("/{post_id}", response_model=PostDisplay, description="Get post by id")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return db_post.get_post(post_id, db)


@router.delete("/{post_id}", description="Delete post by id")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete_post(post_id, db, current_user.id)


@router.post("/image")
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    ext = image.filename.split(".")[1]
    accepted_file_types = ['jpg', 'png', 'JPEG', 'JPG']

    if ext not in accepted_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type error, only '.jpg', .JPG, '.JPEG', '.png' file types allowed")
    if image.size > 2000000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size limit < {format_file_size(2000000)}")

    # Generate a random string to add to the filename to avoid duplication
    letter = string.ascii_letters
    random_string = ''.join(random.choice(letter) for i in range(6))
    new = f"_{random_string}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    # Write the file to the images folder
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {
        'filename': filename,
        'file_size': format_file_size(image.size),
        'file_type': image.content_type,
        'file_path': path
    }
