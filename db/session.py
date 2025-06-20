# Создание асинхронного движка, асинхронной сессии
from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

# Создание асинхронного движка для взаимодействия с бд
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# Создание сессии
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() ->Generator:
    """Зависимость для ..."""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()