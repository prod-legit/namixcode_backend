from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.dependencies import CurrentOrgDep
from app.application.api.schemas.apply import ApplySchema
from app.application.api.schemas.auth import AuthToken
from app.application.api.schemas.org import CreateOrgSchema, OrgSchema
from app.logic.commands.auth.generate_jwt import GenerateJWTUseCase, GenerateJWTCommand
from app.logic.commands.org.create_org import CreateOrgUseCase, CreateOrgCommand
from app.logic.queries.apply.get_org_applies import GetOrgAppliesUseCase, GetOrgAppliesQuery
from app.logic.queries.org.get_orgs import GetOrgsUseCase, GetOrgsQuery

router = APIRouter(
    prefix="/org",
    tags=["Organization"],
    route_class=DishkaRoute
)


@router.post(
    path="/register",
    summary="Регистрация организации",
    operation_id="regOrg",
    status_code=201,
    response_model=AuthToken
)
async def register_org(
        data: CreateOrgSchema,
        create_org: FromDishka[CreateOrgUseCase],
        generate_jwt: FromDishka[GenerateJWTUseCase]
) -> AuthToken:
    org = await create_org.execute(CreateOrgCommand(
        email=data.email,
        password=data.password,
        name=data.name,
        description=data.description,
        location=data.location,
        logo=data.logo,
        foundation_year=data.foundation_year,
        scope=data.scope
    ))
    token = await generate_jwt.execute(GenerateJWTCommand(sub=org.id))

    return AuthToken(token=token)


@router.get(
    path="/me",
    summary="Получить текущую организацию",
    operation_id="getCurrentOrg",
    response_model=OrgSchema
)
async def get_current_org(current_org: CurrentOrgDep) -> OrgSchema:
    return OrgSchema.from_entity(current_org)


@router.get(
    path="/list",
    summary="Получить список организаций",
    operation_id="listOrgs",
    response_model=list[OrgSchema]
)
async def list_orgs(get_orgs: FromDishka[GetOrgsUseCase]) -> list[OrgSchema]:
    orgs = await get_orgs.execute(GetOrgsQuery())
    return [OrgSchema.from_entity(org) for org in orgs]


@router.get(
    path="/applies",
    summary="Получить список откликов",
    operation_id="listApplies",
    response_model=list[ApplySchema]
)
async def get_org_applies(
        current_org: CurrentOrgDep,
        get_applies: FromDishka[GetOrgAppliesUseCase]
) -> list[ApplySchema]:
    applies = await get_applies.execute(GetOrgAppliesQuery(current_org.id))
    return [ApplySchema.from_entity(apply) for apply in applies]
