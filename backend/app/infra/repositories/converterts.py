from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.app_entities import Chat, Message
from app.domain.exceptions.chat import NotUndefinedData
from app.domain.value_objects.app_values import Text, Title

db_mode = "mongoDB"

@dataclass
class BaseConverter(ABC):
    """Базовый интерфейс конвертера чата."""

    @abstractmethod
    def to_document(self):
        """Конвертировать объект в документ для хранения."""
        raise NotImplementedError
    

    @abstractmethod
    def to_entity(self):
        raise NotImplementedError


@dataclass
class ChatMongoDbConverter(BaseConverter):
    """Конвертер Chat/dict для MongoDB."""
    data: Chat | dict

    def to_document(self) -> dict:
        """Преобразовать Chat в словарь для MongoDB."""
        return {
            "chat_id": self.data.uuid,
            "title": self.data.title.as_generic_type(),
            "created_ad": self.data.created_ad
        }
    
    def to_entity(self) -> Chat:
        """Преобразовать dict из MongoDB обратно в Chat."""
        chat = {
            "uuid": self.data.get("chat_id"),
            "title": Title(self.data.get("title")),
            "created_ad": self.data.get("created_ad")
        }
        return Chat(**chat)

@dataclass
class MessageMongoDbConverter(BaseConverter):

    data: Message | dict

    def to_document(self):
        return {
            "chat_id": self.data.chat_id,
            "message_id": self.data.uuid,
            "text": self.data.text.as_generic_type(),
            "created_ad": self.data.created_ad
        } 
    
    def to_entity(self):
        return Message(
            chat_id=self.data.get("chat_id"),
            text=Text(self.data.get("text")),
            uuid=self.data.get("message_id"),
            created_ad=self.data.get("created_ad")
        )

#______________________________________________________ADAPTERS_________________________________________________________________________
def chat_to_valid_data(data: Chat | dict):
    """
    Конвертировать Chat или dict через ChatMongoDbConverter.

    Возвращает dict для Chat и Chat для dict.
    """
    if db_mode == "mongoDB": #МБ в будущем будет postgresql 
        if isinstance(data, Chat):
            return ChatMongoDbConverter(data).to_document()
        elif isinstance(data, dict):
            return ChatMongoDbConverter(data).to_entity()
        else:
            raise NotUndefinedData(type(data))
    return None


def message_to_valid_data(data: Message | dict):
    if db_mode == "mongoDB":
        if isinstance(data, Message):
            return MessageMongoDbConverter(data).to_document()
        elif isinstance(data, dict):
            return MessageMongoDbConverter(data).to_entity()
        else:
            raise NotUndefinedData(type(data))
    
    return None