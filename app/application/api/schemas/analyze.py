from pydantic import BaseModel

from app.domain.entities.analyze import AnalyzeEntity, TaroCardEntity, CosmogramEntity, SuitabilityEntity


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


class AnalyzeSchema(BaseModel):
    cards: list[TaroCardSchema]
    cosmogram: CosmogramSchema
    suitability: SuitabilitySchema

    @classmethod
    def from_entity(cls, entity: AnalyzeEntity) -> "AnalyzeSchema":
        return cls(
            cards=[TaroCardSchema.from_entity(card) for card in entity.cards],
            cosmogram=CosmogramSchema.from_entity(entity.cosmogram),
            suitability=SuitabilitySchema.from_entity(entity.suitability)
        )
