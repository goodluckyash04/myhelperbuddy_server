import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # jwt
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = (
        ""  # node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"  or openssl rand -hex 32
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ENVIRONMENT: str = "local"
    DEBUG: bool = False
    PRODUCTION_MODE: bool = False
    DATABASE_URL: str = "sqlite:///./database.db"

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
