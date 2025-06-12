# Валидация входящего/исходящего (сериализация/де_сериализация) запроса
# Модели, которые исп-ся в самом API. При обработке запроса от пользователя
import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")

class TunedModel(BaseModel):
    class Config:
        """"Говорит pydantic конвертировать в json даже не dict-объекты"""

        orm_model = True

class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    # email: EmailStr
    email: str
    is_active: bool

class UserCreate(BaseModel):
    name: str
    surname: str
    # email: EmailStr
    email: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname should contains only letters")
        return value