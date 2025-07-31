
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SkillHub FastAPI"
    API_V1_STR: str = "/api"

    # JWT settings
    SECRET_KEY: str = "MY_SUPER_SECRET_KEY" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # File Upload settings
    PROFILE_PICS_DIR: str = "static/profile_pics" 

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()