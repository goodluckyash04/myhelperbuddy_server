from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    LOGTAIL_SOURCE_TOKEN: str = os.getenv("LOGTAIL_SOURCE_TOKEN", "")
    LOGTAIL_HOST: str = os.getenv("LOGTAIL_HOST", "")

    class Config:
        print("\tApplication running in",os.getenv('ENVIRONMENT', ''))
        env_file = f".env.{os.getenv('ENVIRONMENT', '')}" if os.getenv('ENVIRONMENT') else ".env"


settings = Settings()
