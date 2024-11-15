from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import BaseEntity


@dataclass
class JWTEntity(BaseEntity):
    sub: str
    issued_at: datetime
    expire_at: datetime
