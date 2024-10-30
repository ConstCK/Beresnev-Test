# Базовая схема для user
from pydantic import BaseModel, Field, ConfigDict


class BaseTask(BaseModel):
    name: str = Field(description='Название задачи')
    description: str = Field(description='Описание задачи')
    status: str = Field(description='Описание задачи')


class Task(BaseTask):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskCreation(BaseTask):
    pass
