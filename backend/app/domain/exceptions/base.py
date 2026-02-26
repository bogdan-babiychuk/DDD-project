from dataclasses import dataclass


@dataclass  
class BaseError(Exception):

    @property
    def message(self) -> str:
        return "Произашла ошибка"
    