"""Модель благотворительного проекта."""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin
from app.models.base import InvestmentMixin

NAME_MAX_LENGTH = 100


class CharityProject(CommonMixin, InvestmentMixin, Base):
    """Благотворительный проект."""

    name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        """Project representation."""
        return f'<CharityProject id={self.id} name={self.name}>'
