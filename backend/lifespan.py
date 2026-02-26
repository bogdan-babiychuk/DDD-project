from app.application.init import init_container
from app.infra.broker.base import BaseBroker


async def start_kafka():
    container = init_container()
    message_broker: BaseBroker = container.resolve(BaseBroker)
    await message_broker.producer.start()


async def close_kafka():
    container = init_container()
    message_broker: BaseBroker = container.resolve(BaseBroker)
    await message_broker.producer.stop()