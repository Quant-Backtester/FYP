# STL
import os
from datetime import timedelta

# External
from dotenv import load_dotenv
from pydantic import BaseModel

# Custom
from custom.custom_enums import RequestEnum




class Settings(BaseModel):
  """Config for the server"""

  load_dotenv(".env", verbose=True)
  # Server
  host: str = "127.0.0.1"
  port: int = 8000
  debug: bool = True

  # Database
  database_url: str = os.getenv(key="DATABASE_URL", default="sqlite:///./app.db")

  # caching
  valkey_url: str = os.getenv(key="VALKEY_URL", default="redis://")

  valkey_port: int = 6379
  valkey_num: int = 0

  # Security
  jwt_secret_key: str = os.getenv(key="JWT_SECRET_KEY", default="default")
  algorithm: str = "HS256"
  access_token_expire_minutes: timedelta = timedelta(minutes=60)
  verify_token_expire_hour: timedelta = timedelta(hours=24)

  # email
  smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
  smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
  smtp_user: str = os.getenv("SMTP_USER", "")
  smtp_password: str = os.getenv("SMTP_PASSWORD", "")

  allowed_origin: list[str] = [
    "http://localhost:5173",
  ]
  allow_methods: list[str] = [method.value for method in RequestEnum]
  allow_headers: list[str] = ["*"]

  # Header fields
  MAX_BODY_LOG_SIZE: int = 1024 * 1024

  SENSITIVE_HEADERS: set[str] = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
    "proxy-authorization",
  }
  SENSITIVE_BODY_FIELDS: set[str] = {
    "password",
    "token",
    "access_token",
    "refresh_token",
    "credit_card",
    "cvv",
    "ssn",
    "secret",
  }

  class Config:
    env_file = ".env"


__all__ = ("Settings",)
