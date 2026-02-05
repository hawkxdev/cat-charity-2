"""Pydantic-схемы для модели CharityProject."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.models.charity_project import NAME_MAX_LENGTH


NAME_MIN_LENGTH = 5
DESCRIPTION_MIN_LENGTH = 10


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""

    name: str = Field(
        ..., min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    description: str = Field(..., min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта."""

    model_config = ConfigDict(extra='forbid')


class CharityProjectUpdate(BaseModel):
    """Схема для обновления проекта."""

    name: Optional[str] = Field(
        None, min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    description: Optional[str] = Field(None, min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: Optional[PositiveInt] = None

    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectBase):
    """Схема проекта из БД."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True, extra='forbid')
