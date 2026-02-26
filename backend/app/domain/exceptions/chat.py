from dataclasses import dataclass, field

from app.domain.exceptions.base import BaseError


@dataclass
class ChatTitleAlreadyExistsError(BaseError):

    title: str

    @property
    def message(self):
        return f"Чат с названием <{self.title}> уже существует"


@dataclass
class ChatNotFoundError(BaseError):

    @property
    def message(self):

        return f"Чата с таким id, не существует"


@dataclass 
class NotUndefinedData(BaseError):

    data: type

    @property
    def message(self):
        return f"Произашла ошибка при конвертации данных в БД: неудачно конвертируемый тип {self.data}"