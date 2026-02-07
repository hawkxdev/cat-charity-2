"""Конфигурация FastAPI Users."""

import logging
from collections.abc import AsyncGenerator
from typing import Annotated, Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
    schemas,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import JWT_LIFETIME_SECONDS, settings
from app.core.db import get_async_session
from app.models.user import User

logger = logging.getLogger(__name__)


async def get_user_db(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """Генератор SQLAlchemyUserDatabase."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """JWT стратегия."""
    return JWTStrategy(
        secret=settings.secret, lifetime_seconds=JWT_LIFETIME_SECONDS
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей."""

    async def validate_password(
        self,
        password: str,
        user: Union[schemas.UC, User],
    ) -> None:
        """Валидация пароля."""
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Пароль должен содержать не менее 3 символов'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не может содержать ваш email'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """Действия после регистрации."""
        logger.info('Пользователь %s зарегистрирован.', user.email)


async def get_user_manager(
    user_db: Annotated[
        SQLAlchemyUserDatabase, Depends(get_user_db)
    ],
) -> AsyncGenerator[UserManager, None]:
    """Корутина для получения UserManager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
