import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    # Маршрут для Postgres
    db_url: str = (f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                   f"@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}")

    host: str = 'localhost'

    # Данные для использования токен-авторизации
    secret_key: str = os.getenv('JWT_SECRET_KEY')
    refresh_secret_key: str = os.getenv('JWT_REFRESH_SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')

    # Настройки для использования переменных из .env
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')


settings = Settings()
