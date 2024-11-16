from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.dependencies import CurrentOrgDep
from app.application.api.schemas.apply import ApplySchema
from app.application.api.schemas.auth import AuthToken
from app.application.api.schemas.employee import EmployeeSchema
from app.application.api.schemas.job import JobSchema, CreateJobSchema
from app.application.api.schemas.org import CreateOrgSchema, OrgSchema, LoginOrgSchema
from app.logic.commands.auth.generate_jwt import GenerateJWTUseCase, GenerateJWTCommand
from app.logic.commands.job.create_job import CreateJobUseCase, CreateJobCommand
from app.logic.commands.org.create_org import CreateOrgUseCase, CreateOrgCommand
from app.logic.queries.apply.get_org_applies import GetOrgAppliesUseCase, GetOrgAppliesQuery
from app.logic.queries.employee.get_org_employees import GetOrgEmployeesUseCase, GetOrgEmployeesQuery
from app.logic.queries.job.get_org_jobs import GetOrgJobsUseCase, GetOrgJobsQuery
from app.logic.queries.org.get_org_auth import GetOrgAuthQuery, GetOrgAuthUseCase
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


@router.post(
    path="/login",
    summary="Вход организации",
    operation_id="loginOrg",
    response_model=AuthToken
)
async def login_org(
        data: LoginOrgSchema,
        auth_org: FromDishka[GetOrgAuthUseCase],
        generate_jwt: FromDishka[GenerateJWTUseCase]
) -> AuthToken:
    org = await auth_org.execute(GetOrgAuthQuery(
        email=data.email,
        password=data.password
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
    operation_id="listOrgApplies",
    response_model=list[ApplySchema]
)
async def get_org_applies(
        current_org: CurrentOrgDep,
        get_applies: FromDishka[GetOrgAppliesUseCase]
) -> list[ApplySchema]:
    applies = await get_applies.execute(GetOrgAppliesQuery(current_org.id))
    return [ApplySchema.from_entity(apply) for apply in applies]


@router.get(
    path="/employees",
    summary="Получить сотрудников",
    operation_id="listOrgEmployees",
    response_model=list[EmployeeSchema]
)
async def get_org_employees(
        current_org: CurrentOrgDep,
        get_employees: FromDishka[GetOrgEmployeesUseCase]
) -> list[EmployeeSchema]:
    employees = await get_employees.execute(GetOrgEmployeesQuery(current_org.id))
    return [EmployeeSchema.from_entity(employee) for employee in employees]


@router.get(
    path="/jobs",
    summary="Получить вакансии",
    operation_id="listOrgJobs",
    response_model=list[JobSchema]
)
async def get_org_jobs(
        current_org: CurrentOrgDep,
        get_jobs: FromDishka[GetOrgJobsUseCase]
) -> list[JobSchema]:
    jobs = await get_jobs.execute(GetOrgJobsQuery(current_org.id))
    return [JobSchema.from_entity(job) for job in jobs]


@router.post(
    path="/job",
    summary="Создать вакансию",
    operation_id="createJob",
    response_model=JobSchema
)
async def create_org_job(
        current_org: CurrentOrgDep,
        data: CreateJobSchema,
        create_job: FromDishka[CreateJobUseCase]
) -> JobSchema:
    job = await create_job.execute(CreateJobCommand(
        org_id=current_org.id,
        title=data.title,
        description=data.description,
        pay=data.pay
    ))
    return JobSchema.from_entity(job)
