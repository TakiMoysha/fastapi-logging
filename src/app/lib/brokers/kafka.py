from logging import getLogger
from dataclasses import dataclass
from typing import AsyncIterator, cast

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from app.domain.events import BaseEvent
from app.lib import Converter
from app.lib.brokers.base import IEventBroker


logger = getLogger(__name__)


@dataclass
class KafkEventBroker(IEventBroker):
    consumer: AIOKafkaConsumer
    producer: AIOKafkaProducer

    async def close(self):
        await self.consumer.stop()
        await self.producer.stop()

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self):
        await self.close()

    async def send(self, key: str, topic: str, msg: bytes):
        await self.producer.send(topic=topic, key=key, value=msg)

    async def subscribe(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            logger.info(f"Received message: {message}")
            event = cast(BaseEvent, message.value)
            yield Converter.from_msg(event)

    async def unsubscribe(self, topic: str):
        self.consumer.unsubscribe()
