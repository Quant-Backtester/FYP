import os

from pydantic import BaseModel

class Settings(BaseModel):
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

    #email
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")

    class Config:
        env_file = ".env"