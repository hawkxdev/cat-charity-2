"""Pydantic-схемы для модели Donation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""

    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""

    model_config = ConfigDict(extra='forbid')


class DonationDB(DonationBase):
    """Схема пожертвования для ответа на POST."""

    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True, extra='forbid')


class DonationFullInfoDB(DonationDB):
    """Схема пожертвования с полной информацией (для GET)."""

    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True, extra='forbid')
