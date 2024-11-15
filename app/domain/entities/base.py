from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class BaseEntity(ABC):
    pass


@dataclass
class IDMixin:
    id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IDMixin):
            return False
        return self.id == other.id
