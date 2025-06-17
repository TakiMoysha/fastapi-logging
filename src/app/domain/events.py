from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import ClassVar
from uuid import UUID, uuid4


@dataclass
class BaseEvent(ABC):
    event_name: ClassVar[str]

    event_id: UUID = field(default_factory=uuid4, kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)


# ================================================
@dataclass
class FeedCreateEvent(BaseEvent):
    event_name: ClassVar[str] = "feed_created"

    channel_id: str
    channel_name: str


@dataclass
class FeedDeleteEvent(BaseEvent):
    event_name: ClassVar[str] = "feed_deleted"

    channel_id: str


# ------------------------------------------------
@dataclass
class NewsPublishEvent(BaseEvent):
    event_name: ClassVar[str] = "news_published"

    news_id: str
    channel_id: str
    content: str


# ------------------------------------------------
@dataclass
class ListenerSubscribeEvent(BaseEvent):
    event_name: ClassVar[str] = "listener_subscribed"

    listener_id: str
    channel_id: str


@dataclass
class ListenerUnsubscribeEvent(BaseEvent):
    event_name: ClassVar[str] = "listener_unsubscribed"

    listener_id: str
