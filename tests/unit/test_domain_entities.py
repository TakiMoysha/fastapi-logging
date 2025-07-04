import pytest

from app.domain.eceptions import BaseDomainException
from app.domain.entities import EntityBuilder, FeedListener


def test_feed_entity_create():
    tom = FeedListener("tom")
    cat = FeedListener("cat")

    feed = EntityBuilder.create_feed("test")

    feed.subscribe(tom)
    feed.subscribe(cat)

    assert len(feed.subscribers) == 2


def test_feed_should_prevent_double_subscription():
    tom = FeedListener("tom")
    feed = EntityBuilder.create_feed("test")

    feed.subscribe(tom)
    with pytest.raises(BaseDomainException):
        feed.subscribe(tom)


def test_feed_should_prevent_actions_after_close():
    tom = FeedListener("tom")
    feed = EntityBuilder.create_feed("test")

    feed.subscribe(tom)
    feed.close()

    with pytest.raises(BaseDomainException):
        feed.subscribe(tom)

    with pytest.raises(BaseDomainException):
        post = EntityBuilder.create_post("title for post", "text for post")
        feed.publish_post(post)
