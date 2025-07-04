from dataclasses import dataclass
from logging import getLogger
from typing import Annotated, AsyncIterator
from typing import cast

import msgspec
import avro
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

    async def send(
        self,
        key: str,
        topic: str,
        msg: bytes,
        *,
        headers: Annotated[dict | None, "Usually support data not related to the domain, ex: trace_id"] = None,
    ):
        await self.producer.send(
            topic=topic,
            key=key,
            value=msg,
            headers=headers,
        )

    async def subscribe(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            logger.info(f"Received message: {message}")
            event = cast(BaseEvent, message.value)
            yield avro.Parser(msgspec).parse(event)

    async def unsubscribe(self, topic: str):
        self.consumer.unsubscribe()
