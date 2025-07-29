# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SkillHub FastAPI"
    API_V1_STR: str = "/api"

    # JWT settings
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_REPLACE_ME" # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # File Upload settings
    PROFILE_PICS_DIR: str = "static/profile_pics" # Path relative to project root

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()