"""Эндпоинты для CharityProject."""

from fastapi import APIRouter

from app.api.validators import (
    check_name_duplicate,
    check_project_before_delete,
    check_project_before_update,
    check_project_exists,
)
from app.core.db import SessionDep
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import (
    close_invested,
    create_project_with_investment,
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(session: SessionDep):
    """Получить список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
):
    """Создать новый проект."""
    await check_name_duplicate(charity_project.name, session)
    return await create_project_with_investment(charity_project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep,
):
    """Обновить проект."""
    project = await check_project_exists(project_id, session)
    await check_project_before_update(project, obj_in.full_amount)
    if obj_in.name is not None and obj_in.name != project.name:
        await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(project, obj_in, session)
    if project.full_amount == project.invested_amount:
        close_invested(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    """Удалить проект."""
    project = await check_project_exists(project_id, session)
    check_project_before_delete(project)
    return await charity_project_crud.remove(project, session)
