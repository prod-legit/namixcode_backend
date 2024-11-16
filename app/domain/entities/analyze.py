from dataclasses import dataclass

from app.domain.entities.base import BaseEntity


@dataclass
class TaroCardEntity(BaseEntity):
    name: str
    meaning: str


@dataclass
class CosmogramEntity(BaseEntity):
    sun_sign: str
    moon_sign: str
    rising_sign: str
    elements: dict[str, str]
    houses: dict[str, str]


@dataclass
class SuitabilityEntity(BaseEntity):
    is_suitable: bool
    explanation: str


@dataclass
class AnalyzeEntity(BaseEntity):
    cards: list[TaroCardEntity]
    cosmogram: CosmogramEntity
    suitability: SuitabilityEntity
