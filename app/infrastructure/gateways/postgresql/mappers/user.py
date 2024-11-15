from app.domain.entities.user import UserEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.models import UserSkillORM, UserInterestORM, UserORM


class UserORMMapper(IORMMapper[UserEntity, UserORM]):
    @staticmethod
    def from_entity(entity: UserEntity) -> UserORM:
        return UserORM(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            name=entity.name,
            phone=entity.phone,
            experience=entity.experience,
            skills=[UserSkillORM(skill=skill) for skill in entity.skills],
            interests=[UserInterestORM(interest=interest) for interest in entity.interests]
        )

    @staticmethod
    def to_entity(orm: UserORM) -> UserEntity:
        return UserEntity(
            id=orm.id,
            email=orm.email,
            hashed_password=orm.hashed_password,
            name=orm.name,
            phone=orm.phone,
            experience=orm.experience,
            skills=[skill.skill for skill in orm.skills],
            interests=[interest.interest for interest in orm.interests]
        )
