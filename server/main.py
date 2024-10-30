from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from config import settings
from initial_tasks import init_models
from routers.users import router as user_router
from routers.tasks import router as task_router


# Создание события при запуске (и остановке) сервера (если нужно)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('starting up...')
    await init_models()
    yield
    print('shutting down...')


# Создание основного приложения
app = FastAPI(
    title='My tasks',
    description='For test...',
    lifespan=lifespan
)

# Включение маршрутов в основное приложение
app.include_router(user_router, tags=['users'])
app.include_router(task_router, tags=['tasks'])


# Приветственный маршрут
@app.get('/', description='Приветственная надпись', )
async def greetings() -> dict:
    return {'message': 'Greetings, sir'}


# Запуск сервера
if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.host, port=8000, reload=True)
