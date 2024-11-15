from app.domain.entities.org import OrgEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.models import OrgORM


class OrgORMMapper(IORMMapper[OrgEntity, OrgORM]):
    @staticmethod
    def from_entity(entity: OrgEntity) -> OrgORM:
        return OrgORM(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            name=entity.name,
            description=entity.description,
            location=entity.location,
            logo=entity.logo,
            foundation_year=entity.foundation_year,
            scope=entity.scope
        )

    @staticmethod
    def to_entity(orm: OrgORM) -> OrgEntity:
        return OrgEntity(
            id=orm.id,
            email=orm.email,
            hashed_password=orm.hashed_password,
            name=orm.name,
            description=orm.description,
            location=orm.location,
            logo=orm.logo,
            foundation_year=orm.foundation_year,
            scope=orm.scope
        )
