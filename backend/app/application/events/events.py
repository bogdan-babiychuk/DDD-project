from dataclasses import dataclass
from typing import ClassVar

from app.application.events.base import BaseEvent


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_id: str
    chat_title: str

@dataclass
class NewMessageRecievedEvent(BaseEvent):
    message_id: str
    message_text: str
    chat_id: str
