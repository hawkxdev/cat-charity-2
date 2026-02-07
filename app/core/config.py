"""Конфигурация приложения."""

from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


JWT_LIFETIME_SECONDS = 3600  # 1 час


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = 'QRKot'
    description: str = 'Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
