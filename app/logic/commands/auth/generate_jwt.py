from dataclasses import dataclass
from datetime import timedelta, datetime, UTC

import jwt

from app.logic.commands.base import ICommand, IUseCase


@dataclass(frozen=True)
class GenerateJWTCommand(ICommand):
    sub: str
    expires_delta: timedelta = timedelta(weeks=4)


@dataclass(eq=False, frozen=True)
class GenerateJWTUseCase(IUseCase[str]):
    secret: str
    algorithm: str

    async def execute(self, command: GenerateJWTCommand) -> str:
        expire = datetime.now(UTC) + command.expires_delta
        jwt_data = {
            "sub": command.sub,
            "iat": datetime.now(UTC),
            "exp": expire
        }
        token = jwt.encode(jwt_data, key=self.secret, algorithm=self.algorithm)
        return token
