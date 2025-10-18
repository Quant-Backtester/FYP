import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """ Config for the server """
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # Security
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "default")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()