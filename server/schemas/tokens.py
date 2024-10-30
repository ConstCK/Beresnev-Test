# Базовая схема для user
from pydantic import BaseModel, Field


class Token(BaseModel):
    token: str

