from dataclasses import dataclass

from app.application.queries.queries import GetChatMessagesQuery, GetChatQuery
from app.domain.exceptions.chat import ChatNotFoundError
from app.infra.repositories.base import BaseChatRepository, BaseMessageRepository


@dataclass
class GetChatQueryHandler:
    chat_repository: BaseChatRepository

    async def handle(self, query: GetChatQuery):
        chat = await self.chat_repository.get_chat_by_uuid(query.chat_id)
        if not chat:
            raise ChatNotFoundError
        return chat
    

@dataclass
class GetChatMessagesQueryHandler:
    chat_repository: BaseMessageRepository

    async def handle(self, query: GetChatMessagesQuery):
        messages = await self.chat_repository.get_messages_by_chat_uuid(query.chat_id)
        if messages is None:
            raise ChatNotFoundError
        return messages