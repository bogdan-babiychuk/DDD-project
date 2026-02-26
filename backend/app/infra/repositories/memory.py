from dataclasses import dataclass

from app.domain.entities.app_entities import Chat, Message
from app.domain.exceptions.chat import ChatNotFoundError
from app.infra.repositories.base import BaseChatRepository, BaseMessageRepository


@dataclass
class BaseMemoryChatRepository(BaseChatRepository):
    chats: dict

    async def create_chat(self, chat: Chat) -> None:
        self.chats[chat.uuid] = chat

    async def get_chat_by_uuid(self, uuid: str):
        return self.chats.get(uuid)

    async def check_exist_chat_by_title(self, title: str) -> bool:
        return any(chat.title.as_generic_type() == title for chat in self.chats.values())


@dataclass
class BaseMemoryMessageRepository(BaseMessageRepository):
    chats: BaseChatRepository

    async def add_message(self, message: Message) -> None:
        chat = await self.chats.get_chat_by_uuid(message.chat_id)
        if chat:
            chat._messages.append(message)
        else:
            raise ChatNotFoundError
    
    async def get_messages_by_chat_uuid(self, chat_uuid: str) -> list[Message]:
        chat = await self.chats.get_chat_by_uuid(chat_uuid)
        if chat:
            sorted_messages = sorted(chat._messages, key=lambda msg: msg.created_ad, reverse=True)
            return sorted_messages
        else:
            raise ChatNotFoundError


