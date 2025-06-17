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
class FeedCreatedEvent(BaseEvent):
    event_name: ClassVar[str] = "feed_created"

    feed_id: str
    feed_title: str


@dataclass
class FeedDeletedEvent(BaseEvent):
    event_name: ClassVar[str] = "feed_deleted"

    feed_id: str


# ------------------------------------------------
@dataclass
class NewsPublishedEvent(BaseEvent):
    event_name: ClassVar[str] = "news_published"

    news_id: str
    feed_id: str
    content: str


# ------------------------------------------------
@dataclass
class ListenerSubscribedEvent(BaseEvent):
    event_name: ClassVar[str] = "listener_subscribed"

    feed_id: str
    listener_id: str


@dataclass
class ListenerUnsubscribedEvent(BaseEvent):
    event_name: ClassVar[str] = "listener_unsubscribed"

    listener_id: str
