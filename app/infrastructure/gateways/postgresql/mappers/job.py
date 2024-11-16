from app.domain.entities.job import JobEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.mappers.org import OrgORMMapper
from app.infrastructure.gateways.postgresql.models import JobORM


class JobORMMapper(IORMMapper[JobEntity, JobORM]):
    @staticmethod
    def from_entity(entity: JobEntity) -> JobORM:
        return JobORM(
            id=entity.id,
            org_id=entity.org.id,
            title=entity.title,
            description=entity.description,
            pay=entity.pay
        )

    @staticmethod
    def to_entity(orm: JobORM) -> JobEntity:
        return JobEntity(
            id=orm.id,
            org=OrgORMMapper.to_entity(orm.org),
            title=orm.title,
            description=orm.description,
            pay=orm.pay
        )
