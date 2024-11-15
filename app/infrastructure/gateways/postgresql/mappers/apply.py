from app.domain.entities.apply import ApplyEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.models import ApplyORM, UserSkillORM, UserInterestORM


class ApplyORMMapper(IORMMapper[ApplyEntity, ApplyORM]):
    @staticmethod
    def from_entity(entity: ApplyEntity) -> ApplyORM:
        return ApplyORM(
            id=entity.id,
            name=entity.name,
            phone=entity.phone,
            email=entity.email,
            experience=entity.experience,
            skills=[UserSkillORM(skill=skill) for skill in entity.skills],
            interests=[UserInterestORM(interest=interest) for interest in entity.interests]
        )

    @staticmethod
    def to_entity(orm: ApplyORM) -> ApplyEntity:
        return ApplyEntity(
            id=orm.id,
            name=orm.name,
            phone=orm.phone,
            email=orm.email,
            experience=orm.experience,
            skills=[skill.skill for skill in orm.skills],
            interests=[interest.interest for interest in orm.interests]
        )
