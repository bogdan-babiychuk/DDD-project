

from dataclasses import dataclass


@dataclass
class GetChatQuery:
    chat_id: str


@dataclass
class GetChatMessagesQuery:
    chat_id: str