from functools import lru_cache
from aiokafka import AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope
from app.infra.repositories.mongodb import ChatMongoDBRepository, MessageMongoDBRepository
from app.settings import settings
from app.application.commands.commands import CreateChatCommand, CreateMessageCommand
from app.application.commands.handlers import CreateChatCommandHandler, CreateMessageCommandHandler
from app.application.mediator.base import Mediator
from app.application.queries.handlers import GetChatMessagesQueryHandler, GetChatQueryHandler
from app.application.queries.queries import GetChatMessagesQuery, GetChatQuery
from app.infra.repositories.base import BaseChatRepository, BaseMessageRepository
from app.infra.repositories.memory import BaseMemoryChatRepository, BaseMemoryMessageRepository
from app.application.events.events import NewChatCreatedEvent, NewMessageRecievedEvent
from app.application.events.handlers import NewChatCreatedHandler, NewMessageRecievedHandler
from app.infra.broker.base import BaseBroker
from app.infra.broker.kafka import KafkaBroker

@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def _init_container():
    container = Container()
     
    container.register(GetChatQueryHandler)
    container.register(GetChatMessagesQueryHandler)

    mongo_client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    

    def _init_Kafka_broker():
        # Создаем broker с настройками таймаутов для предотвращения зависания
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_URL
        )
        return KafkaBroker(producer=producer)

    container.register(BaseBroker, factory=_init_Kafka_broker, scope=Scope.singleton)


    # container.register(NewMessageRecievedHandler)   

    def _init_chat_mongo_db():
        return ChatMongoDBRepository(client=mongo_client,
                                    db_name=settings.MONGO_DB_NAME,
                                    collection=settings.MONGO_DB_CHAT_COLLECTION)
    
    def _init_message_mongo_db():
        return MessageMongoDBRepository(client=mongo_client,
                                        db_name=settings.MONGO_DB_NAME,
                                        collection=settings.MONGO_DB_MESSAGE_COLLECTION)

    # container.register(BaseChatRepository, instance=BaseMemoryChatRepository(chats={}), scope=Scope.singleton)
    container.register(BaseChatRepository, factory=_init_chat_mongo_db, scope=Scope.singleton)
    # container.register(BaseMessageRepository, instance=BaseMemoryMessageRepository(chats=container.resolve(BaseChatRepository)), scope=Scope.singleton)
    container.register(BaseMessageRepository, factory=_init_message_mongo_db, scope=Scope.singleton)

    
    def _init_mediator():
        mediator = Mediator()
        broker = container.resolve(BaseBroker)

        create_chat_handler = CreateChatCommandHandler(_mediator=mediator,
                                                      chat_repository=container.resolve(BaseChatRepository))
        
        create_message_handler = CreateMessageCommandHandler(_mediator=mediator,
                                                             message_repository=container.resolve(BaseMessageRepository),
                                                             chat_repository=container.resolve(BaseChatRepository))
        
        mediator.register_command(CreateChatCommand, [create_chat_handler])
        mediator.register_command(CreateMessageCommand, [create_message_handler])

        mediator.register_query(GetChatQuery, [container.resolve(GetChatQueryHandler)])
        mediator.register_query(GetChatMessagesQuery, [container.resolve(GetChatMessagesQueryHandler)])



        new_chat_created_event_handler = NewChatCreatedHandler(broker=broker, broker_topic=settings.new_chats_event_topic)
        new_message_created_event_handler = NewMessageRecievedHandler(broker=broker, broker_topic=settings.new_message_event_topic) 

        mediator.register_event(NewChatCreatedEvent, [new_chat_created_event_handler])
        mediator.register_event(NewMessageRecievedEvent, [new_message_created_event_handler])
        return mediator
    
    container.register(Mediator, factory=_init_mediator, scope=Scope.singleton)

    return container