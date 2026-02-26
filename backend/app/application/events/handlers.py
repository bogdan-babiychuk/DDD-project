import logging
from dataclasses import dataclass
from app.application.events.base import BaseEventHandler
from app.application.events.events import NewChatCreatedEvent, NewMessageRecievedEvent
from app.infra.broker.base import BaseBroker
from app.infra.broker.converters import convert_event_to_broker_message

logger = logging.getLogger(__name__)

@dataclass
class NewChatCreatedHandler(BaseEventHandler):
    broker: BaseBroker
    broker_topic: str

    async def handle(self, event: NewChatCreatedEvent):
        try:
            await self.broker.publish(
                topic=self.broker_topic,
                value=convert_event_to_broker_message(event),
                key=str(event.event_id).encode()
            )
        except Exception as e:
            logger.error(f"Failed to send chat creation event to Kafka: {e}")


@dataclass
class NewMessageRecievedHandler(BaseEventHandler):
    
    broker: BaseBroker
    broker_topic: str

    async def handle(self, event: NewMessageRecievedEvent):
        try:
            await self.broker.publish(
                topic=self.broker_topic,
                value=convert_event_to_broker_message(event),
                key=str(event.event_id).encode()
            )
        except Exception as e:
            logger.error(f"Failed to send message creation to Kafka: {e}")
