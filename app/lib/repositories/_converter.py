"""
Converter using inside the repository, u don't need to use it
"""

from dataclasses import asdict
from typing import TYPE_CHECKING, Protocol, Sequence, Union, cast, overload, runtime_checkable

import msgspec

from app.domain.events import BaseEvent
from app.lib import OffsetPagination


@runtime_checkable
class IModel(Protocol):
    if TYPE_CHECKING:
        __collection_name__: str
        __model_name__: str

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, any]: ...


class ResultConverter:
    ...
    # @overload
    # def to_model(self, data: "IModel", operation: str | None = None) -> any:
    #     """parse and convert input into a model."""

    # @overload
    # def to_model(self, data: any, operaiton: str | None = None) -> any:
    #     pass

    # @overload
    # def to_schema(
    #     self,
    #     data: "Sequence[IModel]",
    #     *args,
    #     **kwargs,
    # ) -> Union["Sequence[IModel]", dict]: ...

    # @overload
    # def to_schema(
    #     self,
    #     data: "Sequence[IModel]",
    #     total: int | None = None,
    #     filters: Sequence[any] | None = None,
    #     *,
    #     schema_type: type | None = None,
    # ) -> Union[list[dict], dict]:
    #     """Convert the object to a response schema
    #
    #     when `schema_type` is None, the model is returned with no conversion.
    #
    #     Args:
    #         data: ...
    #             type: :class:`~app.lib.repositories...`
    #         total: The total count of the data
    #         filters: :class:``
    #         schema_type: The schema to convert the data to
    #
    #     Raises:
    #         BaseAppError: if `schema_type` is not a valid Msgspec or Pydantic (fastapi) schema.
    #
    #     Returns:
    #         :clas:`app.base.IModel` | :class:`msgspec.Struct` | :class:`pydantic.BaseModel`
    #     """
    #
    #     if filters is None:
    #         filters = []
    #
    #     if schema_type is None:
    #         if not isinstance(data, Sequence):
    #             return cast(type(data), data) # type: ignore[unreachable,unused-ignore]
    #
    #         # limit_offset = find_filter(LimitOffset, filster=filters)
    #         # totla = total or len(data)
    #         # limit_offset = limit_offset if limit_offset is not None else LimitOffset(limit=len(data), offset=0)
    #         return OffsetPagination[](
    #             items=cast(type(data), data), # type: ignore[unreachable,unused-ignore]
    #             limit=limit_offset.limit,
    #             offset=limit_offset.offset,
    #             total=totla
    #         )
    #
    #     if MSGSCPEC_INSTALLED:
    #         return msgspec.json.decode(schema_type, data)
    #
    #
    #     msg = "`schema_type` should be a valid Msgspec or Pydantic schema."
    #     raise BaseAppError(msg)
