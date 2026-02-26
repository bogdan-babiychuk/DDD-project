from dataclasses import dataclass

from app.application.commands.base import BaseCommand


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):

    chat_id: str
    text: str