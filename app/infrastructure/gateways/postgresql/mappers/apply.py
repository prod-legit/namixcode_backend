from app.domain.entities.apply import ApplyEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.mappers.org import OrgORMMapper
from app.infrastructure.gateways.postgresql.mappers.user import UserORMMapper
from app.infrastructure.gateways.postgresql.models import ApplyORM


class ApplyORMMapper(IORMMapper[ApplyEntity, ApplyORM]):
    @staticmethod
    def from_entity(entity: ApplyEntity) -> ApplyORM:
        return ApplyORM(
            id=entity.id,
            org_id=entity.org.id,
            user_id=entity.user.id,
            date=entity.date
        )

    @staticmethod
    def to_entity(orm: ApplyORM) -> ApplyEntity:
        return ApplyEntity(
            id=orm.id,
            org=OrgORMMapper.to_entity(orm.org),
            user=UserORMMapper.to_entity(orm.user),
            date=orm.date
        )
