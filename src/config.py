from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


def get_model_config(env_dir: str = f"{BASE_DIR}/.env"):
    config = SettingsConfigDict(
        env_file=env_dir, env_file_encoding="utf-8", extra="ignore"
    )
    return config


class DBSettings(BaseSettings):
    host: str = Field(alias="DB_HOST")
    port: str = Field(alias="DB_PORT")
    name: str = Field(alias="DB_NAME")
    user: str = Field(alias="DB_USER")
    password: str = Field(alias="DB_PASS")

    model_config = get_model_config()


class Settings(BaseSettings):
    debug: bool = Field(alias="DEBUG", default=True)
    host: str = Field(alias="API_HOST", default="localhost")
    port: int = Field(alias="API_PORT", default=8000)
    secret: SecretStr = Field(alias="SECRET_KEY")

    origins: List[str] = Field(alias="API_ORIGINS")

    _db: DBSettings = None

    model_config = get_model_config()

    @property
    def db(self) -> DBSettings:
        if self._db is None:
            self._db = DBSettings()
        return self._db


@lru_cache()
def get_config():
    return Settings()
