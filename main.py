from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from db import models
from db.database import engine
from routes.user_routes import user_routes
from routes.post_routes import post_routes
from routes.comment_routes import comment_routes
from auth.authentication import router as auth_router

# Load the env variables
load_dotenv()
SERVER_PORT = int(os.environ.get("SERVER_PORT"))

# Create the app
app = FastAPI(title="InstaBlogger API", description="InstaBlogger rest api", version="0.1.0")
# Routes
app.include_router(auth_router)
app.include_router(user_routes.router)
app.include_router(post_routes.router)
app.include_router(comment_routes.router)

# Make images folder statically available
app.mount('/images', StaticFiles(directory='images'), name='images')

# CORS
origins = [
    'localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


# Create the DB on first run
models.Base.metadata.create_all(engine)

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", port=SERVER_PORT, reload=True)
