
from dataclasses import dataclass

from app.application.commands.base import BaseCommandHandler
from app.application.commands.commands import CreateChatCommand, CreateMessageCommand
from app.domain.entities.app_entities import Chat, Message
from app.domain.exceptions.chat import ChatNotFoundError, ChatTitleAlreadyExistsError
from app.domain.value_objects.app_values import Text, Title
from app.infra.repositories.base import BaseChatRepository, BaseMessageRepository


@dataclass
class CreateChatCommandHandler(BaseCommandHandler):
    chat_repository: BaseChatRepository
    
    async def handle(self, command: CreateChatCommand):
        if await self.chat_repository.check_exist_chat_by_title(command.title):
            raise ChatTitleAlreadyExistsError(command.title)
        
        title = Title(command.title)
        new_chat = Chat.create_chat(title=title)
        await self.chat_repository.create_chat(chat=new_chat)
        await self._mediator.handle_events(new_chat.pull_events())
        return new_chat


@dataclass
class CreateMessageCommandHandler(BaseCommandHandler):
    message_repository: BaseMessageRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateMessageCommand):
        if not await self.chat_repository.get_chat_by_uuid(command.chat_id):
            raise ChatNotFoundError
        
        text = Text(command.text)
        message = Message.create_message(chat_id=command.chat_id, text=text)
        await self.message_repository.add_message(message=message)
        await self._mediator.handle_events(message.pull_events())
        return message
