from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Any

import jwt

from app.domain.entities.auth import JWTEntity
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.auth import (
    InvalidJWTPayloadException,
    InvalidAuthTokenException,
    AuthTokenExpired
)


@dataclass(frozen=True)
class DecodeJWTCommand(ICommand):
    token: str


@dataclass(eq=False, frozen=True)
class DecodeJWTUseCase(IUseCase[JWTEntity]):
    secret: str
    algorithm: str

    async def execute(self, command: DecodeJWTCommand) -> JWTEntity:
        try:
            decoded_jwt: dict[str, Any] = jwt.decode(
                jwt=command.token, key=self.secret, algorithms=[self.algorithm]
            )
        except jwt.PyJWTError:
            raise InvalidAuthTokenException(token=command.token)

        if (
                "sub" not in decoded_jwt
                or "iat" not in decoded_jwt
                or "exp" not in decoded_jwt
        ):
            raise InvalidJWTPayloadException(
                token=command.token, payload=decoded_jwt
            )

        jwt_data = JWTEntity(
            sub=decoded_jwt["sub"],
            issued_at=datetime.fromtimestamp(decoded_jwt["iat"], UTC),
            expire_at=datetime.fromtimestamp(decoded_jwt["exp"], UTC),
        )

        if jwt_data.expire_at < datetime.now(UTC):
            raise AuthTokenExpired(
                token=command.token, expired_at=jwt_data.expire_at
            )

        return jwt_data
