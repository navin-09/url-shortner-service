# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    BASE_URL: str
    SHORT_CODE_LENGTH: int = Field(8, env="SHORT_CODE_LENGTH")

    class Config:
        env_file = ".env"

settings = Settings()
