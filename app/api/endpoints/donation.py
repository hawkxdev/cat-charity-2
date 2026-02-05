"""Эндпоинты для Donation."""

from fastapi import APIRouter

from app.core.db import SessionDep
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import create_donation_with_investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
)
async def get_all_donations(session: SessionDep):
    """Получить список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
):
    """Создать пожертвование."""
    return await create_donation_with_investment(donation, session)
