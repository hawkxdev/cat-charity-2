"""Сервис инвестирования."""

from datetime import datetime
from typing import Sequence, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationCreate

InvestmentModel = Union[CharityProject, Donation]


def close_invested(obj: InvestmentModel) -> None:
    """Пометить объект закрытым."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


def distribute_funds(
    source: InvestmentModel,
    targets: Sequence[InvestmentModel],
) -> None:
    """FIFO распределение средств."""
    for target in targets:
        if source.fully_invested:
            break

        available = source.full_amount - source.invested_amount
        needed = target.full_amount - target.invested_amount
        transfer = min(available, needed)

        source.invested_amount += transfer
        target.invested_amount += transfer

        if source.invested_amount >= source.full_amount:
            close_invested(source)

        if target.invested_amount >= target.full_amount:
            close_invested(target)


async def create_project_with_investment(
    project_data: CharityProjectCreate,
    session: AsyncSession,
) -> CharityProject:
    """Создать проект и распределить пожертвования (одна транзакция)."""
    new_project = await charity_project_crud.create(
        project_data, session, commit=False
    )
    donations = await donation_crud.get_not_fully_invested(session)
    distribute_funds(new_project, donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


async def create_donation_with_investment(
    donation_data: DonationCreate,
    session: AsyncSession,
    user: User,
) -> Donation:
    """Создать пожертвование и распределить по проектам (одна транзакция)."""
    new_donation = await donation_crud.create(
        donation_data, session, user=user, commit=False
    )
    projects = await charity_project_crud.get_not_fully_invested(session)
    distribute_funds(new_donation, projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
