"""Абстрактный миксин для моделей."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column


class InvestmentMixin:
    """Общие поля для CharityProject и Donation."""

    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, index=True
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
