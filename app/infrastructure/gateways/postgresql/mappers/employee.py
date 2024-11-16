from app.domain.entities.employee import EmployeeEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.mappers.job import JobORMMapper
from app.infrastructure.gateways.postgresql.mappers.user import UserORMMapper
from app.infrastructure.gateways.postgresql.models import EmployeeORM


class EmployeeORMMapper(IORMMapper[EmployeeEntity, EmployeeORM]):
    @staticmethod
    def from_entity(entity: EmployeeEntity) -> EmployeeORM:
        return EmployeeORM(
            id=entity.id,
            job_id=entity.job.id,
            user_id=entity.user.id,
            head_id=entity.head.id if entity.head else None,
            slaves=[EmployeeORMMapper.from_entity(slave) for slave in entity.slaves],
            date=entity.date
        )

    @staticmethod
    def to_entity(orm: EmployeeORM, recursion: bool = True) -> EmployeeEntity:
        return EmployeeEntity(
            id=orm.id,
            job=JobORMMapper.to_entity(orm.job),
            user=UserORMMapper.to_entity(orm.user),
            head=EmployeeORMMapper.to_entity(orm.head) if orm.head and recursion else None,
            slaves=[EmployeeORMMapper.to_entity(slave, recursion=False) for slave in orm.slaves] if recursion else [],
            date=orm.date
        )
