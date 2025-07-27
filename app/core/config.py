import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./database.db"
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    LOGTAIL_SOURCE_TOKEN: str = ""
    LOGTAIL_HOST: str = ""

    class Config:
        # Automatically loads env file only when not on Render
        env_file = (
            f".env.{os.getenv('ENVIRONMENT', 'local')}"
            if not os.getenv("RENDER")
            else None
        )
        env_file_encoding = "utf-8"


settings = Settings()
