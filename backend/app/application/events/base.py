from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import uuid4

from app.infra.broker.base import BaseBroker


@dataclass(kw_only=True)
class BaseEvent(ABC):
    event_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default=datetime.utcnow())


@dataclass
class BaseEventHandler(ABC):

    broker: BaseBroker
    broker_topic: str 

    @abstractmethod
    def handle(event:BaseEvent):
        ...
    