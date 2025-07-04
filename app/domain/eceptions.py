from dataclasses import dataclass


@dataclass(eq=False)
class BaseDomainException(Exception):
    msg: str

    @property
    def message(self):
        if self.msg:
            return self.msg
        return "DomainException"
