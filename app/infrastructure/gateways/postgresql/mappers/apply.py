from app.domain.entities.apply import ApplyEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.mappers.job import JobORMMapper
from app.infrastructure.gateways.postgresql.mappers.user import UserORMMapper
from app.infrastructure.gateways.postgresql.models import ApplyORM


class ApplyORMMapper(IORMMapper[ApplyEntity, ApplyORM]):
    @staticmethod
    def from_entity(entity: ApplyEntity) -> ApplyORM:
        return ApplyORM(
            id=entity.id,
            job_id=entity.job.id,
            user_id=entity.user.id,
            date=entity.date
        )

    @staticmethod
    def to_entity(orm: ApplyORM) -> ApplyEntity:
        return ApplyEntity(
            id=orm.id,
            job=JobORMMapper.to_entity(orm.job),
            user=UserORMMapper.to_entity(orm.user),
            date=orm.date
        )
