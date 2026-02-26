from dataclasses import dataclass
from app.consts import MAX_TEXT_LENGTH
from app.domain.exceptions.text import TextEmptyError, TextTooLongError
from app.domain.value_objects.base import BaseValueObject


@dataclass
class Text(BaseValueObject):
    value: str

    def validate(self):
        if self.value == "":
            raise TextEmptyError
        
        if len(self.value) > MAX_TEXT_LENGTH:
            raise TextTooLongError

    def as_generic_type(self):
        return str(self.value)
    


@dataclass
class Title(BaseValueObject):
    value: str

    def validate(self):
        if self.value == "":
            raise TextEmptyError
        
        if len(self.value) > MAX_TEXT_LENGTH:
            raise TextTooLongError(length_text=len(self.value))
    
    def as_generic_type(self):
        return str(self.value)
    