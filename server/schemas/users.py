from pydantic import BaseModel, ConfigDict, Field


# Базовая схема для user
class BaseUser(BaseModel):
    username: str = Field(min_length=4, max_length=24,
                          description='Имя пользователя')


# Схема для получения user
class User(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Схема для создания user и получения token
class UserCreation(BaseUser):
    password: str = Field(description='Пароль пользователя',
                          min_length=4,
                          max_length=16)


# Схема для итогового user
class UserResult(User):
    password: str = Field(description='Хэшированный пароль пользователя')

    model_config = ConfigDict(from_attributes=True)
