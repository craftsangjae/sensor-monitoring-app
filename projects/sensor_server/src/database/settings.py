from pydantic_settings import BaseSettings
from pydantic import Field


class DatabaseSettings(BaseSettings):
    DB_TYPE: str = Field(default="postgresql")
    DB_NAME: str = Field()
    DB_USER: str = Field()
    DB_PASSWORD: str = Field()
    DB_HOST: str = Field()
    DB_PORT: int = Field(default=5432)
    DB_ECHO: bool = Field(default=False)
