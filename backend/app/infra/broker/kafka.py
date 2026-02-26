
from dataclasses import dataclass
from aiokafka import AIOKafkaProducer
from app.infra.broker.base import BaseBroker

@dataclass
class KafkaBroker(BaseBroker):
    
    producer: AIOKafkaProducer

    async def publish(self, key:bytes, topic:str, value: bytes):
        try:
            await self.producer.send(topic=topic, key=key, value=value)
        except Exception as e:
            # Логируем ошибку, но не прерываем выполнене
            print(f"Failed to publish message to Kafka: {e}")
            # Можно добавить fallback механизм здесь (например, сохранение в локальную очередь)