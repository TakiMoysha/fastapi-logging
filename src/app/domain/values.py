from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Self, TypeVar


VT = TypeVar("VT", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[VT]):
    value: VT

    def __post_init__(self):
        self.validate()

    @classmethod
    @abstractmethod
    def from_value(cls, value: VT): ...
    @abstractmethod
    def validate(self): ...
    @abstractmethod
    def as_generic_type(self): ...


@dataclass(frozen=True)
class Text(BaseValueObject[str]):
    @classmethod
    def from_value(cls, value: Self | str):
        match value:
            case str():
                return Text(value=value)
            case Text():
                value.validate()
                return value
            case _:
                raise ValueError(f"ValueObject:Text invalid value: {value}")

    def validate(self):
        if not self.value:
            raise ValueError("ValueObject:Text cannot be empty")

    def as_generic_type(self):
        return self.value


@dataclass(frozen=True)
class Title(BaseValueObject[str]):
    _max_lenght = 100

    @classmethod
    def from_value(cls, value: Self | str):
        match value:
            case str():
                return Title(value=value)
            case Title():
                value.validate()
                return value
            case _:
                raise ValueError(f"ValueObject:Title invalid value: {value}")

    def validate(self):
        if not self.value:
            raise ValueError("ValueObject:Title cannot be empty")

        if len(self.value) > self._max_lenght:
            raise ValueError(f"ValueObject:Title cannot be longer than {self._max_lenght} characters")

    def as_generic_type(self):
        return self.value
