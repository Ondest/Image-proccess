from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


class DBHandler:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url, future=True)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def _init_tests_db(self, url: str):
        self.engine = create_async_engine(
            url,
            poolclass=NullPool,
            future=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_handler = DBHandler(settings.db_url)
