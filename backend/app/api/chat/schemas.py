from datetime import datetime
from pydantic import BaseModel

from app.domain.entities.app_entities import Chat, Message

class ChatResponseSchema(BaseModel):
    chat_id: str
    title: str
    created_ad: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatResponseSchema':
        return cls(
            chat_id=chat.uuid,
            title=chat.title.as_generic_type(),
            created_ad=chat.created_ad 

        )

class CreateChatRequesteSchema(BaseModel):
    title: str


class AddMessageRequestSchema(BaseModel):
    text:str

class CreatedMessageResponseSchema(BaseModel):
    chat_id: str
    message_id: str
    text: str
    created_ad: datetime

    @classmethod
    def from_entity(cls, message: Message) -> 'CreatedMessageResponseSchema':
        return cls(
            chat_id=message.chat_id,
            message_id=message.uuid,
            text=message.text.as_generic_type(),
            created_ad=message.created_ad
        )




class ChatMessagesResponseSchema(BaseModel):
    chat_id: str
    messages: list[CreatedMessageResponseSchema]

    @classmethod
    def from_entity(cls, chat_id: str,
                    messages: list[Message]) -> 'ChatMessagesResponseSchema':
        return cls(
            chat_id=chat_id,
            messages=[CreatedMessageResponseSchema.from_entity(msg) for msg in messages]
        )
    
    
class BaseSchemaError(BaseModel):
    error: str