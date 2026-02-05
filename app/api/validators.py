"""Валидаторы для API."""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject

ERROR_NAME_DUPLICATE = 'Проект с таким именем уже существует!'
ERROR_PROJECT_NOT_FOUND = 'Проект не найден!'
ERROR_PROJECT_HAS_INVESTMENTS = (
    'В проект были внесены средства, не подлежит удалению!'
)
ERROR_PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
ERROR_AMOUNT_TOO_LOW = 'Нельзя установить сумму меньше уже вложенной!'


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверить уникальность имени."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail=ERROR_NAME_DUPLICATE,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверить существование проекта."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=ERROR_PROJECT_NOT_FOUND,
        )
    return project


def check_project_before_delete(
    project: CharityProject,
) -> None:
    """Проверить что проект можно удалить."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=ERROR_PROJECT_HAS_INVESTMENTS,
        )


async def check_project_before_update(
    project: CharityProject,
    new_full_amount: Optional[int],
) -> None:
    """Проверить что проект можно редактировать."""
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=ERROR_PROJECT_CLOSED,
        )
    if new_full_amount is not None:
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=400,
                detail=ERROR_AMOUNT_TOO_LOW,
            )
