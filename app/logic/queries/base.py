from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True)
class BaseQuery(ABC):
    pass


QT = TypeVar("QT", bound=BaseQuery)
QR = TypeVar("QR")


@dataclass(eq=False, frozen=True)
class BaseQueryHandler[QT, QR](ABC):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        pass
