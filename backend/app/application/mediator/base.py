
from dataclasses import dataclass
from app.application.mediator.command import CommandMediator
from app.application.mediator.event import EventMediator
from app.application.mediator.query import QueryMediator


@dataclass
class Mediator(CommandMediator, EventMediator, QueryMediator):
    ...