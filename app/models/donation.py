"""Модель пожертвования."""

from typing import Optional

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin
from app.models.base import InvestmentMixin


class Donation(CommonMixin, InvestmentMixin, Base):
    """Пожертвование."""

    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        """Donation representation."""
        return f'<Donation id={self.id} amount={self.full_amount}>'
