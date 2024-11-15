from app.domain.entities.user import UserEntity
from app.infrastructure.gateways.postgresql.mappers.base import IORMMapper
from app.infrastructure.gateways.postgresql.models import UserProfessionORM, UserInterestORM, UserORM


class UserORMMapper(IORMMapper[UserEntity, UserORM]):
    @staticmethod
    def from_entity(entity: UserEntity) -> UserORM:
        return UserORM(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            name=entity.name,
            phone=entity.phone,
            sex=entity.sex,
            birthdate=entity.birthdate,
            experience=entity.experience,
            professions=[UserProfessionORM(profession=profession) for profession in entity.professions],
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
            sex=orm.sex,
            birthdate=orm.birthdate,
            experience=orm.experience,
            professions=[profession.profession for profession in orm.professions],
            interests=[interest.interest for interest in orm.interests]
        )
