from abc import ABC, abstractmethod

from app.domain.entities.base import BaseEntity
from app.infrastructure.gateways.postgresql.models.base import BaseORM


class IORMMapper[E: BaseEntity, O: BaseORM](ABC):
    @staticmethod
    @abstractmethod
    def from_entity(entity: E) -> O: ...

    @staticmethod
    @abstractmethod
    def to_entity(orm: O) -> E: ...
