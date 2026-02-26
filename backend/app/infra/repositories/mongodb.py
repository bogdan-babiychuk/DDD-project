

from abc import ABC
from dataclasses import dataclass
from app.domain.entities.app_entities import Chat, Message
from app.infra.repositories.base import BaseChatRepository, BaseMessageRepository
from motor.motor_asyncio import AsyncIOMotorClient

from app.infra.repositories.converterts import chat_to_valid_data, message_to_valid_data


@dataclass
class BaseMongoDBRepository(ABC):
    client: AsyncIOMotorClient
    db_name: str
    collection: str

    @property
    def _collection(self):
        return self.client[self.db_name][self.collection]


@dataclass
class ChatMongoDBRepository(BaseChatRepository, BaseMongoDBRepository):

    async def create_chat(self, chat: Chat) -> None:

        await self._collection.insert_one(chat_to_valid_data(chat))
    

    async def get_chat_by_uuid(self, uuid: str):
        chat_data = await self._collection.find_one({"chat_id": uuid})
        if chat_data:
            return chat_to_valid_data(chat_data)
        return None


    async def check_exist_chat_by_title(self, title: str) -> bool:
        chat_data = await self._collection.find_one({"title": title})
        return chat_data is not None
    
    
class MessageMongoDBRepository(BaseMessageRepository, BaseMongoDBRepository):

    async def add_message(self, message: Message):
        await self._collection.insert_one(message_to_valid_data(message))


    async def get_messages_by_chat_uuid(self, chat_uuid: str) -> list[Message]:
        chat_messages = await self._collection.find({"chat_id": chat_uuid}).sort("created_ad", -1).to_list(length=None)
        result = [message_to_valid_data(message) for message in chat_messages]
        return result
    

