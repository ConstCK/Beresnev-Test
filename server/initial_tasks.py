# Создание таблиц в БД при запуске приложения
from database.db import engine, Base


# Создание моделей в БД при запуске сервера
async def init_models() -> None:
    async with engine.begin() as conn:
        # Создание таблиц в БД
        await conn.run_sync(Base.metadata.create_all)
