import asyncio
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable
import logging

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from src.database.base import Base
from src.exceptions import DatabaseException, NotFoundException, DBIntegrityException
from src.database.settings import DatabaseSettings

logger = logging.getLogger(__name__)


class SessionFactory:
    """비동기 데이터베이스 클래스"""

    def __init__(self, settings: DatabaseSettings):
        logger.info(f"initialize SessionFactory({settings.DB_TYPE})")
        if settings.DB_TYPE.startswith("postgresql"):
            url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
            self._engine = create_async_engine(url, echo=settings.DB_ECHO)
        else:
            raise DatabaseException(
                f"지원하지 않는 database type입니다. {settings.DB_TYPE}"
            )

        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                bind=self._engine,
            ),
            scopefunc=asyncio.current_task,
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def __call__(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except sqlalchemy.exc.NoResultFound:
            await session.rollback()
            raise NotFoundException("데이터를 못발견했아요")
        except sqlalchemy.exc.IntegrityError:
            await session.rollback()
            raise DBIntegrityException("데이터를 못발견했아요")
        except Exception as e:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise e
        finally:
            await session.close()
            await self._session_factory.remove()

    async def connect(self):
        return await self._engine.connect()
