from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Движок для связи с БД
engine = create_async_engine(settings.db_url, echo=True)
# Сессия для связи с БД
async_session = async_sessionmaker(
    bind=engine, autocommit=False, autoflush=False)


# Создание класса-родителя для наследования при создании моделей
class Base(DeclarativeBase):
    pass


# Создание генератора сессии
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
