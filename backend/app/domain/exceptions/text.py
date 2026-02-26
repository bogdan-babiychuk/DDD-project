

from dataclasses import dataclass
from app.consts import MAX_TEXT_LENGTH
from app.domain.exceptions.base import BaseError


class TextEmptyError(BaseError):

    @property
    def message(self):
        return f"Текст не может быть пустым"

@dataclass
class TextTooLongError(BaseError):

    length_text: int

    @property
    def message(self):
        return f"Введённая строка имеет {self.length_text} символов, а максимально допустимое количество символов: {MAX_TEXT_LENGTH}"
