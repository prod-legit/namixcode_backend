from pydantic import BaseModel

from app.domain.entities.analyze import TaroCardEntity, CosmogramEntity, SuitabilityEntity, \
    CompareAnalyzeEntity, SuitableAnalyzeEntity, CompatibilityEntity, UserAnalyzeEntity


class TaroCardSchema(BaseModel):
    name: str
    meaning: str

    @classmethod
    def from_entity(cls, entity: TaroCardEntity) -> "TaroCardSchema":
        return cls(name=entity.name, meaning=entity.meaning)


class CosmogramSchema(BaseModel):
    sun_sign: str
    moon_sign: str
    rising_sign: str
    elements: dict[str, str]
    houses: dict[str, str]

    @classmethod
    def from_entity(cls, entity: CosmogramEntity) -> "CosmogramSchema":
        return cls(
            sun_sign=entity.sun_sign,
            moon_sign=entity.moon_sign,
            rising_sign=entity.rising_sign,
            elements=entity.elements,
            houses=entity.houses
        )


class SuitabilitySchema(BaseModel):
    is_suitable: bool
    explanation: str

    @classmethod
    def from_entity(cls, entity: SuitabilityEntity) -> "SuitabilitySchema":
        return cls(is_suitable=entity.is_suitable, explanation=entity.explanation)


class CompatibilitySchema(BaseModel):
    score: int
    explanation: str

    @classmethod
    def from_entity(cls, entity: CompatibilityEntity) -> "CompatibilitySchema":
        return cls(score=entity.score, explanation=entity.explanation)


class UserAnalyzeSchema(BaseModel):
    cards: list[TaroCardSchema]
    cosmogram: CosmogramSchema

    @classmethod
    def from_entity(cls, entity: UserAnalyzeEntity) -> "UserAnalyzeSchema":
        return cls(
            cards=[TaroCardSchema.from_entity(card) for card in entity.cards],
            cosmogram=CosmogramSchema.from_entity(entity.cosmogram)
        )


class SuitableAnalyzeSchema(UserAnalyzeSchema):
    suitability: SuitabilitySchema

    @classmethod
    def from_entity(cls, entity: SuitableAnalyzeEntity) -> "SuitableAnalyzeSchema":
        return cls(
            cards=[TaroCardSchema.from_entity(card) for card in entity.cards],
            cosmogram=CosmogramSchema.from_entity(entity.cosmogram),
            suitability=SuitabilitySchema.from_entity(entity.suitability)
        )


class CompareAnalyzeSchema(BaseModel):
    boss: UserAnalyzeSchema
    employee: UserAnalyzeSchema
    compatibility: CompatibilitySchema

    @classmethod
    def from_entity(cls, entity: CompareAnalyzeEntity) -> "CompareAnalyzeSchema":
        return cls(
            boss=UserAnalyzeSchema.from_entity(entity.boss),
            employee=UserAnalyzeSchema.from_entity(entity.employee),
            compatibility=CompatibilitySchema.from_entity(entity.compatibility)
        )


class AtmosphereAnalyzeSchema(CompareAnalyzeSchema):
    pass
