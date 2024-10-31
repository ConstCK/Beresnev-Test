from typing import Annotated

from fastapi import APIRouter, status, Depends


from crud.users import UserService
from schemas.tokens import Token
from schemas.users import UserCreation


# Маршрут Регистрации и авторизации
router = APIRouter(prefix='/api/v1/auth')


# Маршрут для регистрации нового пользователя с получением токенов
@router.post('/register', description='Registration',
             status_code=status.HTTP_201_CREATED, name='user_registration',
             responses={201: {'description': 'Успешная регистрация'},
                        409: {'description': 'Пользователь уже существует'}}
             )
async def signup(data: UserCreation, service: Annotated[UserService, Depends()]) -> dict[str, str]:
    result = await service.create_user(data)
    return result


# Вход в систему при использовании username&password с получением токенов
@router.post('/login', description='Authorization',
             status_code=status.HTTP_200_OK, name='user_authorization_by_username',
             responses={200: {'description': 'Успешное авторизация'},
                        401: {'description': 'Ошибка авторизации'}}
             )
async def login(data: UserCreation, service: Annotated[UserService, Depends()] ) -> dict[str, str]:
    result = await service.login_user(data)
    return result


# Получение нового access token, используя refresh token
@router.post('/refresh', description='Getting new access token',
             status_code=status.HTTP_200_OK, name='new_access_token',
             responses={200: {'description': 'Успешное получение токена'},
                        401: {'description': 'Ошибка авторизации'}}
             )
async def get_access(token: Token, service: Annotated[UserService, Depends()]) -> dict[str, str]:
    result = await service.get_new_token(token.token)
    return result


