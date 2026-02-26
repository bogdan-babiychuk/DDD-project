from typing import Annotated, Container
from fastapi import APIRouter, HTTPException, Path, Query
from fastapi import status

from app.api.chat.dependencies import ConteinerDep
from app.api.chat.schemas import AddMessageRequestSchema, BaseSchemaError, ChatMessagesResponseSchema, ChatResponseSchema, CreateChatRequesteSchema, CreatedMessageResponseSchema
from app.application.commands.commands import CreateChatCommand, CreateMessageCommand
from app.application.queries.queries import GetChatMessagesQuery, GetChatQuery
from app.domain.exceptions.base import BaseError
from app.application.mediator.base import Mediator

router = APIRouter(tags=["Чаты"])


@router.post(
    "/",
    summary="Создание нового чата",
    description=(
        "Создаёт новый чат. "
        "Если чат с таким названием уже существует — возвращает ошибку 400."
    ),
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": BaseSchemaError,
            "description": "Чат с таким названием уже существует",
        },
        status.HTTP_201_CREATED: {
            "model": ChatResponseSchema,
            "description": "Успешное создание чат",
        },
    },
)
async def create_chat_handler(
    request: CreateChatRequesteSchema,
    container: ConteinerDep
) -> ChatResponseSchema | None:
    mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(
            CreateChatCommand(title=request.title)
        )
    except BaseError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": err.message},
        )
    return ChatResponseSchema.from_entity(chat=chat)


@router.post(
    "/{chat_id}/messages",
    summary="Создание сообщения для чата",
    description="",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": BaseSchemaError,
            "description": "Чата с таким id не существует"
        },
        status.HTTP_201_CREATED: {
            "model": CreatedMessageResponseSchema,
            "description": "Успешное создание сообщения"
        }
    }
)
async def create_message_handler(chat_id: Annotated[str, Path(description="Нужно ввести id чата")],
                                 request: AddMessageRequestSchema,
                                 container: ConteinerDep):
        
    mediator = container.resolve(Mediator)
    try:
        command = CreateMessageCommand(chat_id=chat_id,
                                       text=request.text)
        message, *_ = await mediator.handle_command(command)
    except BaseError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": err.message},
        )
    return CreatedMessageResponseSchema.from_entity(message=message)



@router.get(
    "/{chat_id}/",
    summary="Получение чата",
    description=("Получаем существующий чат, если нет то 400."),
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": ChatResponseSchema,
            "description": "Успешное получение чата",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": BaseSchemaError,
            "description": "Ошибка при получение чата:\n",
        },
    },
)
async def get_chat(
    chat_id: Annotated[
        str,
        Path(
            description="Нужно ввести object id чата",
            example="b09ca3d0-80cb-42af-8bcf-a5c037a82de7",
        ),
    ],
    container: ConteinerDep,
):
    mediator = container.resolve(Mediator)
    try:
        query = GetChatQuery(chat_id=chat_id)
        chat, *_ = await mediator.handle_query(query)
    except BaseError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": err.message}
        )
    return ChatResponseSchema.from_entity(chat)


@router.get(
    "/{chat_id}/messages",
    summary="Получение сообщений в чате",
    description="",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": BaseSchemaError,
            "description": "Чата с таким id не существует"
        },
        status.HTTP_200_OK: {
            "model": CreatedMessageResponseSchema,
            "description": "Успешное получение сообщений"
        }
    }
)
async def get_chat_messages(
    chat_id: Annotated[
        str,
        Path(
            description="Нужно ввести object id чата",
            example="b09ca3d0-80cb-42af-8bcf-a5c037a82de7",
        ),
    ],
    container: ConteinerDep):
    mediator = container.resolve(Mediator)
    try:
        query = GetChatMessagesQuery(chat_id=chat_id)
        messages, *_= await mediator.handle_query(query)
    except BaseError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": err.message}
        )  
    return ChatMessagesResponseSchema.from_entity(chat_id=chat_id, messages=messages)