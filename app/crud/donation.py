"""CRUD для Donation."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationCreate]):
    """CRUD для пожертвований."""

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> Sequence[Donation]:
        """Получить пожертвования пользователя."""
        result = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
