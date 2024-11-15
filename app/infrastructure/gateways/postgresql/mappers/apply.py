from app.domain.entities.apply import ApplyEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.models import ApplyORM


class ApplyORMMapper(IORMMapper[ApplyEntity, ApplyORM]):
    @staticmethod
    def from_entity(entity: ApplyEntity) -> ApplyORM:
        return ApplyORM(
            org_id=entity.org_id,
            user_id=entity.user_id,
            date=entity.date
        )

    @staticmethod
    def to_entity(orm: ApplyORM) -> ApplyEntity:
        return ApplyEntity(
            org_id=orm.org_id,
            user_id=orm.user_id,
            date=orm.date
        )
