# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.routers import api_router
from src.core.config import settings
from src.db.connection import create_db_and_tables # Import for dev/testing
from pathlib import Path
import os
from src.core.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or use ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],            # allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # allow all headers
)


Path(settings.PROFILE_PICS_DIR).mkdir(parents=True, exist_ok=True)
app.mount(
    "/static/profile_pics",
    StaticFiles(directory=settings.PROFILE_PICS_DIR),
    name="profile_pics"
)

app.include_router(api_router)



@app.get("/")
def read_root():

    return {"message": "Welcome to SkillHub FastAPI Backend!"}

@app.get("/log-test")
async def log_test():
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    return {"message": "Logged successfully!"}

@app.get("/hello")
def read_hello():
    return {"message": "Hello World"}
