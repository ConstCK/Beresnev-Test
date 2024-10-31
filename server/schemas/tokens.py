from pydantic import BaseModel, Field


# Базовая схема для token
class Token(BaseModel):
    token: str
