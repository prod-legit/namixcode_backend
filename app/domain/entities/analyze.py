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
class CompatibilityEntity(BaseEntity):
    score: int
    explanation: str


@dataclass
class UserAnalyzeEntity(BaseEntity):
    name: str
    cards: list[TaroCardEntity]
    cosmogram: CosmogramEntity


@dataclass
class SuitableAnalyzeEntity(UserAnalyzeEntity):
    cards: list[TaroCardEntity]
    cosmogram: CosmogramEntity
    suitability: SuitabilityEntity


@dataclass
class CompareAnalyzeEntity(BaseEntity):
    boss: UserAnalyzeEntity
    employee: UserAnalyzeEntity
    compatibility: CompatibilityEntity


@dataclass
class CompareListEntity(BaseEntity):
    best_match: CompareAnalyzeEntity
    other_matches: list[CompareAnalyzeEntity]


@dataclass
class EmployeeAtmosphereAnalyzeEntity(BaseEntity):
    name: str
    main_analytics: str
    compatibility_score: int
    impact_on_atmosphere: str


@dataclass
class AtmosphereAnalyzeEntity(BaseEntity):
    overall_analysis: str
    employees: list[EmployeeAtmosphereAnalyzeEntity]
