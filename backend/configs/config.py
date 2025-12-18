# STL

# External
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Custom
from custom.custom_enums import RequestEnum


class Settings(BaseSettings):
  """Config for the server"""

  # Server
  host: str = "127.0.0.1"
  port: int = 8000
  debug: bool = True

  # Database
  database_url: str = "sqlite:///./app.db"

  # caching
  valkey_scheme: str = "redis://"
  valkey_host: str = "127.0.0.1"

  valkey_port: int = 6379
  valkey_db: int = 0

  # Security
  jwt_secret_key: str = "1234"
  algorithm: str = "HS256"
  access_token_expire_minutes: int = 60
  verify_token_expire_hour: int = 24

  # email
  smtp_host: str = "smtp.gmail.com"
  smtp_port: int = 465
  smtp_user: str = ""
  smtp_password: str = ""

  allowed_origin: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

  allow_methods: list[str] = Field(
    default_factory=lambda: [method.value for method in RequestEnum]
  )
  allow_headers: list[str] = Field(default_factory=lambda: ["*"])

  # Header fields
  max_body_log_size: int = 1024 * 1024

  sensitive_headers: set[str] = Field(
    default_factory=lambda: {
      "authorization",
      "cookie",
      "set-cookie",
      "x-api-key",
      "x-auth-token",
      "proxy-authorization",
    }
  )
  sensitive_body_fields: set[str] = Field(
    default_factory=lambda: {
      "password",
      "token",
      "access_token",
      "refresh_token",
      "credit_card",
      "cvv",
      "ssn",
      "secret",
    }
  )

  model_config = SettingsConfigDict(env_file=".env")


__all__ = ("Settings",)
