from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from task_management.settings.settings import settings

async_engine: AsyncEngine = create_async_engine(
    str(settings.db.url),
    echo=True,
    connect_args={"prepared_statement_cache_size": 0},
)

async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
