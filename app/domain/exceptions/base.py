from dataclasses import asdict, dataclass
from typing import Any


@dataclass(eq=False, frozen=True)
class AppException(Exception):
    def __str__(self) -> str:
        return "An error occurred during the application execution"

    @property
    def meta(self) -> dict[str, Any]:
        return asdict(self)
