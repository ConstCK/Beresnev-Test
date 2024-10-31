import datetime
from typing import Annotated

from fastapi import HTTPException, status, Depends, Header
from passlib.context import CryptContext
from jose import jwt, JWTError

from config import settings
from database.redis import TokenRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
repository = TokenRepository()


# Хеширование чистого пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Проверка соответствия чистого пароля хеш-паролю
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Создания access токена для пользователя
def create_access_token(data: dict[str, str]) -> str:
    exp = datetime.datetime.now() + datetime.timedelta(minutes=60)
    secret_key = settings.secret_key
    payload = {'sub': data['id'], 'exp': exp}
    encode_jwt = jwt.encode(claims=payload,
                            key=secret_key,
                            algorithm=settings.algorithm)
    return encode_jwt


# Создания refresh токена для пользователя с сохранением в БД (redis)
async def create_refresh_token(data: dict[str, str]) -> str:
    exp = datetime.datetime.now() + datetime.timedelta(days=30)
    secret_key = settings.refresh_secret_key
    payload = {'sub': data['id'], 'exp': exp}
    encode_jwt = jwt.encode(claims=payload,
                            key=secret_key,
                            algorithm=settings.algorithm)
    await repository.set_token(data['id'], encode_jwt)
    return encode_jwt


# Валидация access токена
def validate_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token=token, key=settings.secret_key, algorithms=settings.algorithm)
        # Проверка JWT токена на истечение срока годности
        if not datetime.datetime.now() > (
                datetime.datetime.fromtimestamp(payload.get('exp'))):
            return payload.get('sub')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен больше не действителен!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')


# Валидация refresh токена
async def validate_refresh_token(token: str) -> str:
    try:
        payload = jwt.decode(token=token, key=settings.refresh_secret_key,
                             algorithms=settings.algorithm)
        saved_token = await repository.get_token(payload.get('sub'))
        if token == saved_token:
            return payload.get('sub')
        raise JWTError
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')


def access_granted(token: Annotated[str, Header()], ) -> str | None:
    result = validate_access_token(token)
    return result if result else None
