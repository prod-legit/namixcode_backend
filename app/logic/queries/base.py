from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class IQuery(ABC):  # noqa: B024
    pass


@dataclass(eq=False, frozen=True)
class IUseCase[T](ABC):
    @abstractmethod
    async def execute(self, query: IQuery) -> T:
        pass
