import datetime
from typing import Annotated

from fastapi import HTTPException, status, Depends, Request, Header
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/signup")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хеширование чистого пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Проверка соответствия чистого пароля хеш-паролю
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Создания токена для пользователя
def create_token(data: dict[str, str], token_type: str = 'access', ) -> str:
    if token_type == 'access':
        exp = datetime.datetime.now() + datetime.timedelta(minutes=60)
        secret_key = settings.secret_key
    else:
        exp = datetime.datetime.now() + datetime.timedelta(days=30)
        secret_key = settings.refresh_secret_key

    payload = {'sub': data['id'], 'exp': exp}
    encode_jwt = jwt.encode(claims=payload,
                            key=secret_key,
                            algorithm=settings.algorithm)
    return encode_jwt


# Валидация токена
def validate_token(token: str, token_type: str = 'access') -> str:
    secret_key = settings.secret_key if token_type == 'access' else settings.refresh_secret_key

    try:
        payload = jwt.decode(token=token, key=secret_key, algorithms=settings.algorithm)
        # Проверка JWT токена на истечение срока годности
        if not datetime.datetime.now() > (
                datetime.datetime.fromtimestamp(payload.get('exp'))):
            return payload.get('sub')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен больше не действителен!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')


def access_granted(token: Annotated[str, Header()],) -> str | None:
    result = validate_token(token)
    return result if result else None
