from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.entities.org import OrgEntity
from app.domain.entities.user import UserEntity
from app.logic.commands.auth.decode_jwt import DecodeJWTCommand, DecodeJWTUseCase
from app.logic.exceptions.auth import EmptyAuthTokenException
from app.logic.queries.org.get_org import GetOrgQuery, GetOrgUseCase
from app.logic.queries.user.get_user import GetUserUseCase, GetUserQuery


@inject
async def get_current_org(
        token: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(HTTPBearer(scheme_name="org", auto_error=False))
        ],
        decode_jwt: FromDishka[DecodeJWTUseCase],
        get_org: FromDishka[GetOrgUseCase],
) -> OrgEntity:
    if token is None:
        raise EmptyAuthTokenException()

    jwt_data = await decode_jwt.execute(DecodeJWTCommand(token=token.credentials))
    org = await get_org.execute(GetOrgQuery(org_id=jwt_data.sub))

    return org


CurrentOrgDep = Annotated[OrgEntity, Depends(get_current_org)]


@inject
async def get_current_user(
        token: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(HTTPBearer(scheme_name="user", auto_error=False))
        ],
        decode_jwt: FromDishka[DecodeJWTUseCase],
        get_user: FromDishka[GetUserUseCase],
) -> UserEntity:
    if token is None:
        raise EmptyAuthTokenException()

    jwt_data = await decode_jwt.execute(DecodeJWTCommand(token=token.credentials))
    user = await get_user.execute(GetUserQuery(user_id=jwt_data.sub))

    return user


CurrentUserDep = Annotated[UserEntity, Depends(get_current_user)]
