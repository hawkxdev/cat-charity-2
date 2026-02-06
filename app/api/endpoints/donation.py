"""Эндпоинты для Donation."""

from fastapi import APIRouter, Depends

from app.core.db import SessionDep
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import create_donation_with_investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(session: SessionDep):
    """Получить список всех пожертвований (только суперпользователь)."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Получить список пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(session, user)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Создать пожертвование."""
    return await create_donation_with_investment(donation, session, user)
