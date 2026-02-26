from dataclasses import dataclass, field

from app.application.events.events import NewChatCreatedEvent, NewMessageRecievedEvent
from app.domain.entities.base import BaseEntity

from app.domain.value_objects.app_values import Text, Title


@dataclass
class Message(BaseEntity):
    chat_id: str
    text: Text

    @classmethod
    def create_message(cls,
                       chat_id: str,
                       text: Text) -> 'Message':
        
        message = cls(chat_id=chat_id, text=text)

        message.register_event(
            NewMessageRecievedEvent(
                message_id=message.uuid,
                message_text=message.text.as_generic_type(),
                chat_id=message.chat_id)
        )
        return message


@dataclass
class Chat(BaseEntity):
    title: Title
    _messages: list[Message] = field(default_factory=list, kw_only=True)


    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(
            NewChatCreatedEvent(
                chat_id=new_chat.uuid,
                chat_title=title.as_generic_type(),
            )
        )
        return new_chat






