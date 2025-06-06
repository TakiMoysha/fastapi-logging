# ruff: noqa: E402
# =================================================================
from dataclasses import asdict
from typing_extensions import deprecated

import msgspec

from app.domain.events import BaseEvent


@deprecated("use `app.lib.repositories.converter:ResultConverter`")
class Converter:
    __slots__ = ()

    @classmethod
    def into_msg(cls, event: BaseEvent) -> bytes:
        return msgspec.json.encode(event)

    @classmethod
    def from_msg(cls, event: BaseEvent) -> dict[str, any]:
        return asdict(event)


# =================================================================

from typing import Protocol


class IAsyncContextManagerMixin(Protocol):
    async def __aenter__(self): ...
    async def __aexit__(self): ...


# =================================================================

from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class OffsetPagination(Generic[T]):
    __slots__ = ("items", "limit", "offset", "total")

    items: Sequence[T]

    limit: int
    offset: int

    total: int


# =================================================================
