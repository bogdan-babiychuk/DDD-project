
from abc import ABC
from dataclasses import dataclass, field

from app.application.events.base import BaseEvent, BaseEventHandler




@dataclass
class EventMediator(ABC):

    _events_map: dict[BaseEvent, list[BaseEventHandler]] = field(default_factory=dict)

    def register_event(self, event_type: BaseEvent, handler: BaseEventHandler):
        self._events_map[event_type] = handler


    async def handle_events(self, event_list: list[BaseEvent]):
        for event in event_list:
            handlers = self._events_map.get(type(event))
            for handler in handlers:
                await handler.handle(event)

