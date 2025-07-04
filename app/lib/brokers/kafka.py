from dataclasses import dataclass
from functools import lru_cache
from logging import getLogger
from typing import Annotated, AsyncIterator
from typing import cast

import msgspec
from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer

from app.domain.events import BaseEvent
from app.lib.brokers.base import IEventBroker

logger = getLogger(__name__)


MessageSchema = {
    "type": "record",
    "name": "Message",
    "fields": [
        {"name": "event_name", "type": "string"},
        {"name": "event_id", "type": "string"},
        {"name": "created_at", "type": "string"},
    ],
}


class KafkaEventConverter:
    def encode(self, event_model: BaseEvent) -> bytes:
        return msgspec.json.encode(event_model.__dict__)

    def decode(self, data: bytes) -> BaseEvent:
        decoded_dict = msgspec.json.decode(data)
        return BaseEvent(**decoded_dict)


@dataclass
class KafkEventBroker(IEventBroker):
    consumer: AIOKafkaConsumer
    producer: AIOKafkaProducer

    # converter = KafkaEventConverter()
    #
    # @property
    # @lru_cache
    # def up_consumer(self, bootstrap_servers: str) -> AIOKafkaConsumer:
    #     return AIOKafkaConsumer(
    #         bootstrap_servers=bootstrap_servers,
    #         value_deserializer=self.converter.decode,
    #     )
    #
    # @property
    # @lru_cache
    # def up_producer(self, bootstrap_servers: str) -> AIOKafkaProducer:
    #     return AIOKafkaProducer(
    #         bootstrap_servers=bootstrap_servers,
    #         value_serializer=self.converter.encode,
    #     )

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

    async def send(
        self,
        key: str,
        topic: str,
        event: BaseEvent,
        *,
        headers: Annotated[dict | None, "Usually support data not related to the domain, ex: trace_id"] = None,
    ):
        await self.producer.send(
            topic=topic,
            key=key,
            value=KafkaEventConverter().encode(event),
            headers=headers,
        )

    async def subscribe(self, topic: str) -> AsyncIterator[BaseEvent]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            logger.info(f"Received message: {message}")
            yield KafkaEventConverter().decode(cast(bytes, message.value))

    async def unsubscribe(self, topic: str):
        self.consumer.unsubscribe()
