from abc import ABC
from dataclasses import dataclass, field
import datetime
from uuid import uuid4

from app.application.events.base import BaseEvent



@dataclass
class BaseEntity(ABC):

    uuid: str = field(default_factory=lambda:str(uuid4()), kw_only=True)
    created_ad: datetime = field(default_factory=datetime.datetime.now, kw_only=True)
    _events: list[BaseEvent] = field(default_factory=list, kw_only=True)

    def register_event(self, event: BaseEvent):
        self._events.append(event)

    def pull_events(self):
        events = self._events.copy()
        self._events.clear()
        return events
    

    def __hash__(self):
        return hash(self.uuid)
    
    def __eq__(self, value: "BaseEntity"):
        return  self.uuid == value.uuid