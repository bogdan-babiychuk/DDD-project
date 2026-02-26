from abc import ABC, abstractmethod
from mailbox import Message

from app.domain.entities.app_entities import Chat


class BaseChatRepository(ABC):
    
    @abstractmethod
    def create_chat(self, chat: Chat) -> None:
        ...

    @abstractmethod
    def get_chat_by_uuid(self, uuid: str):
        ...
    
    @abstractmethod
    def check_exist_chat_by_title(self, title: str):
        ...
   
   
class BaseMessageRepository(ABC):

    @abstractmethod
    def add_message(self, message: Message) -> None:
        ...

    @abstractmethod
    def get_messages_by_chat_uuid(self, chat_uuid: str) -> list[Message]:
        ...
    
