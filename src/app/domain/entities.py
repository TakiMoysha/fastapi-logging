"""or maybe DAO..."""

from abc import ABC
from copy import copy
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Self
from uuid import uuid4

from app.domain.eceptions import BaseDomainException
from app.domain.values import Text, Title

from .events import BaseEvent, FeedCreatedEvent, FeedDeletedEvent, ListenerSubscribedEvent


# ================================================================================
@dataclass
class AuditEntityMixin:
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    updated_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )


@dataclass
class EventsFunctionalityMixin:
    _events: list[BaseEvent] = field(
        default_factory=list,
        kw_only=True,
    )

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = copy(self._events)
        self._events.clear()

        return registered_events


# ================================================================================


@dataclass
class BaseEntity(ABC, EventsFunctionalityMixin):
    id: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: "BaseEntity") -> bool:
        return self.id == __value.id


# ================================================================================


@dataclass(eq=False)
class Feed(BaseEntity, AuditEntityMixin):
    title: Title

    news: set["News"] = field(default_factory=set, kw_only=True)
    subscribers: set["FeedListener"] = field(default_factory=set, kw_only=True)

    is_closed: bool = field(default=False, kw_only=True)

    @classmethod
    def create(cls, title: Title | str) -> Self:
        _feed = cls(title=Title.from_value(title))
        _feed.register_event(
            FeedCreatedEvent(
                feed_id=_feed.id,
                feed_title=_feed.title.as_generic_type(),
            ),
        )

        return _feed

    def close(self):
        self.is_closed = True
        self.register_event(FeedDeletedEvent(feed_id=self.id))

    def push_news(self, news: "News"):
        if self.is_closed:
            raise BaseDomainException("Feed is closed")

        self.news.add(news)
        self.register_event(ListenerSubscribedEvent(feed_id=self.id, listener_id=news.id))

    def subscribe(self, listener: "FeedListener"):
        if self.is_closed:
            raise BaseDomainException("Feed is closed")

        if listener in self.subscribers:
            raise BaseDomainException("Listener already subscribed")

        self.subscribers.add(listener)
        self.register_event(ListenerSubscribedEvent(feed_id=self.id, listener_id=listener.id))

    def unsubscribe(self, listener: "FeedListener"):
        if listener not in self.subscribers:
            raise BaseDomainException("Listener not subscribed")

        self.subscribers.remove(listener)
        self.register_event(ListenerSubscribedEvent(feed_id=self.id, listener_id=listener.id))


@dataclass(eq=False)
class News(BaseEntity):
    title: Title
    text: Text


@dataclass(eq=False)
class FeedListener(BaseEntity): ...
