from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True)
class BaseCommand(ABC):
    pass


CT = TypeVar("CT", bound=BaseCommand)
CR = TypeVar("CR")

@dataclass(eq=False, frozen=True)
class BaseCommandHandler[CT, CR](ABC):
    @abstractmethod
    async def handle(self, command: CT) -> CR:
        pass
