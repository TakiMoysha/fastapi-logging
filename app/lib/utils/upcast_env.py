# !TODO: enums, Literals

import os
from pathlib import Path
from typing import Annotated, Callable, Final, cast, overload, Self

__VERSION__ = Final[0.1]

TRUE_VALUES = ("1", "t", "true", "y", "yes")
PATH_SEPARATOR = ":"
BOOTSTRAP_SEPARATOR = ";"

type TParse = str | bool | int | Path | BootstrapAddress


class BootstrapAddress:
    def __init__(self, value: list[str] | None = None) -> None:
        self.value = value if value is not None else list()

    @classmethod
    def from_raw(cls, value: str) -> Self:
        return cls(value.split(BOOTSTRAP_SEPARATOR))


type TBootstrap = Annotated[BootstrapAddress, BootstrapAddress.from_raw]

type T = type


@overload
def get_upcast_env(key: str, default: str, type_hint: None = None) -> str: ...
@overload
def get_upcast_env(key: str, default: bool, type_hint: None = None) -> bool: ...
@overload
def get_upcast_env(key: str, default: int, type_hint: None = None) -> int: ...
@overload
def get_upcast_env(key: str, default: Path, type_hint: None = None) -> Path: ...
@overload
def get_upcast_env(key: str, default: BootstrapAddress, type_hint: None = None) -> BootstrapAddress: ...
@overload
def get_upcast_env(key: str, default: None, type_hint: None = None) -> None: ...


def get_upcast_env(
    key: str,
    default: TParse | None,
    type_hint: type[T] | None = None,
) -> TParse | T | None:
    """Environement variable parser

    Args:
        key: environment variable
        default: default value
        type_hint: by default inferring from default value

    Raises:
        ValueError: value cannot be parsed

    Returns:
        parsed value of the specified type
    """

    str_value = os.getenv(key)

    if str_value is None:
        return cast("T", default) if type_hint is not None else default

    value: str = str_value

    if type(default) is str:
        return cast("T", value) if type_hint is not None else value

    if type(default) is bool:
        _in = value.lower() in TRUE_VALUES
        return cast("T", _in) if type_hint is not None else _in

    if type(default) is int:
        _in = int(value)
        return cast("T", _in) if type_hint is not None else _in

    if isinstance(default, Path):
        _in = Path(value)
        return cast("T", _in) if type_hint is not None else _in

    if isinstance(default, BootstrapAddress):
        _in = BootstrapAddress.from_raw(value)
        return cast("T", _in) if type_hint is not None else _in

    msg = f"Cannot parse value: [{key}<{type(default)}>]: {value}"
    raise ValueError(msg)


# *TODO:
# def upcast_env_functor(
#     key: str,
#     default: TParse | None,
#     type_hint: type[T] | None = None,
# ) -> Callable[[], TParse | T | None]:
#     def functor() -> TParse | T | None:
#         return get_upcast_env(key, default, type_hint)
#
#     return functor
