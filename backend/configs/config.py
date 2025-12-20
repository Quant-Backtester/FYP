# STL

# External
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field

# Custom
from common.enums import RequestEnum


class Settings(BaseSettings):
  """Config for the server"""

  model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
  # Server
  host: str
  port: int
  debug: bool = True

  # Database
  database: str
  database_password: str
  database_username: str
  database_host: str
  database_port: int
  database_driver: str

  @computed_field
  @property
  def database_url(self) -> str:
    return (
      f"{self.database_driver}://"
      f"{self.database_username}:"
      f"{self.database_password}@"
      f"{self.database_host}:"
      f"{self.database_port}/"
      f"{self.database}"
    )

  # caching
  valkey_scheme: str
  valkey_host: str

  valkey_port: int
  valkey_db: int

  

  @computed_field
  @property
  def valkey_url(self) -> str:
    return f"{self.valkey_scheme}://{self.valkey_host}:{self.valkey_port}/{self.valkey_db}"

  # Security
  jwt_secret_key: str
  algorithm: str
  access_token_expire_hour:str

  @property
  def access_token_expire_hour(self,) -> int:
    return int()
  remember_me_expire_day: int

  # email
  smtp_host: str
  smtp_port: int
  smtp_user: str
  smtp_password: str

  allowed_origin: list[str]

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
