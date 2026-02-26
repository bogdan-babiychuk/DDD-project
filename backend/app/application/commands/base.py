from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.application.mediator.event import EventMediator


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...

@dataclass
class BaseCommandHandler(ABC):

    _mediator: EventMediator

    @abstractmethod
    def handle(self, command: BaseCommand):
        ...
    
