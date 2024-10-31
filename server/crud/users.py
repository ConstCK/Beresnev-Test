from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from database.redis import TokenRepository
from models.models import User as UserTable
from schemas.users import User, UserCreation
from services.auth import (get_password_hash, create_access_token, create_refresh_token,
                           verify_password, validate_refresh_token)

repository = TokenRepository()
class UserService:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.db = session

    # Получение списка всех пользователей
    async def get_users(self) -> list[User] | list:
        query = select(UserTable)
        users = await self.db.execute(query)
        result = users.scalars().all()
        return list(result)

    # Создание пользователя(регистрация)
    async def create_user(self, data: UserCreation) -> dict[str, str]:
        query = select(UserTable).where(UserTable.username == data.username)
        db_user = await self.db.execute(query)
        result = db_user.scalar()
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')

        hashed_password = get_password_hash(data.password)
        db_user = UserTable(username=data.username,
                            password=hashed_password,
                            )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        query = select(UserTable).where(UserTable.username == data.username)
        db_user = await self.db.execute(query)
        user = db_user.scalar()

        access_token = create_access_token({'id': str(user.id)})
        refresh_token = await create_refresh_token({'id': str(user.id)})
        return {'message': 'Регистрация прошла успешно',
                'user': user.username,
                'access': access_token,
                'refresh': refresh_token}

    # Аутентификация пользователя (проверка name&password)
    async def _authenticate_user(self, data: UserCreation) -> User | None:
        query = select(UserTable).where(UserTable.username == data.username)
        db_user = await self.db.execute(query)
        user = db_user.scalar()
        if (not user or
                verify_password(plain_password=data.password,
                                hashed_password=user.password) is False):
            return None
        return user

    # Логин по username и паролю
    async def login_user(self, data: UserCreation) -> dict[str, str]:
        db_user = await self._authenticate_user(data)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Неверное имя или пароль')

        access_token = create_access_token({'id': str(db_user.id)})
        refresh_token = await create_refresh_token({'id': str(db_user.id)})

        return {'message': 'Успешный вход в систему',
                'user': db_user.username,
                'access': access_token,
                'refresh': refresh_token}

    @staticmethod
    async def get_new_token(token: str) -> dict:
        try:
            result = await validate_refresh_token(token=token)
            access_token = create_access_token({'id': str(result)})
            refresh_token = await create_refresh_token({'id': str(result)})
            return {'access': access_token,
                    'refresh': refresh_token}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Ошибка при создании нового токена')
