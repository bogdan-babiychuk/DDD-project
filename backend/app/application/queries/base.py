
from abc import ABC, abstractmethod

class BaseQuery(ABC):
    pass


class BaseQueryHandler(ABC):

    @abstractmethod
    def handle(self, query: BaseQuery):
        ...




