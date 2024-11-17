from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path
from pydantic import UUID4

from app.application.api.dependencies import CurrentUserDep, CurrentOrgDep
from app.application.api.schemas.analyze import SuitableAnalyzeSchema, CompareAnalyzeSchema, AtmosphereAnalyzeSchema, CompareListSchema
from app.application.api.schemas.apply import ApplySchema, CreateApplySchema, AcceptApplySchema
from app.application.api.schemas.status import StatusSchema
from app.infrastructure.services.gpt_tarologue import IGPTTarologue
from app.logic.commands.apply.accept_apply import AcceptApplyUseCase, AcceptApplyCommand
from app.logic.commands.apply.create_apply import CreateApplyUseCase, CreateApplyCommand
from app.logic.queries.employee.get_org_employees import GetOrgEmployeesUseCase, GetOrgEmployeesQuery
from app.logic.queries.user.get_user import GetUserUseCase, GetUserQuery

router = APIRouter(
    prefix="/apply",
    tags=["Apply"],
    route_class=DishkaRoute
)


@router.post(
    path="",
    summary="Отправить отклик на вакансию",
    operation_id="makeApply",
    status_code=201,
    response_model=ApplySchema
)
async def make_apply(
        current_user: CurrentUserDep,
        data: CreateApplySchema,
        create_apply: FromDishka[CreateApplyUseCase]
) -> ApplySchema:
    apply = await create_apply.execute(CreateApplyCommand(
        job_id=str(data.job_id),
        user_id=current_user.id
    ))

    return ApplySchema.from_entity(apply)


@router.post(
    path="/{user_id}/accept",
    summary="Принять на работу",
    operation_id="acceptApply",
    response_model=StatusSchema
)
async def accept_user_apply(
        current_org: CurrentOrgDep,
        user_id: Annotated[UUID4, Path()],
        data: AcceptApplySchema,
        accept_apply: FromDishka[AcceptApplyUseCase]
) -> StatusSchema:
    await accept_apply.execute(AcceptApplyCommand(
        # job_id=current_org.id,
        user_id=user_id,
        head_id=data.head_id
    ))
    return StatusSchema.success("User applied")


@router.post(
    path="/suitability/{user_id}",
    summary="Подходит ли пользователь по таро",
    operation_id="userSuitabilityTaro",
    response_model=SuitableAnalyzeSchema
)
async def suitability_user_taro(
        current_org: CurrentOrgDep,
        user_id: Annotated[UUID4, Path()],
        get_user: FromDishka[GetUserUseCase],
        gpt_tarologue: FromDishka[IGPTTarologue]
) -> SuitableAnalyzeSchema:
    user = await get_user.execute(GetUserQuery(user_id=user_id))
    analyze = await gpt_tarologue.suitable_analyze(user)

    return SuitableAnalyzeSchema.from_entity(analyze)


@router.post(
    path="/compare/{user_id}/{boss_id}",
    summary="Подходит ли пользователь к начальнику по таро",
    operation_id="compareUserBossTaro",
    response_model=CompareAnalyzeSchema
)
async def compare_user_boss_taro(
        current_org: CurrentOrgDep,
        user_id: Annotated[UUID4, Path()],
        boss_id: Annotated[UUID4, Path()],
        get_user: FromDishka[GetUserUseCase],
        gpt_tarologue: FromDishka[IGPTTarologue]
) -> CompareAnalyzeSchema:
    user = await get_user.execute(GetUserQuery(user_id=user_id))
    boss = await get_user.execute(GetUserQuery(user_id=boss_id))
    analyze = await gpt_tarologue.compare_analyze(user=user, boss=boss)

    return CompareAnalyzeSchema.from_entity(analyze)


@router.post(
    path="/compare_collective/{user_id}",
    summary="Подходит ли пользователь коллективу",
    operation_id="compareUserCollectiveTaro",
    response_model=CompareListSchema
)
async def compare_user_collective(
        current_org: CurrentOrgDep,
        user_id: Annotated[UUID4, Path()],
        get_user: FromDishka[GetUserUseCase],
        get_employees: FromDishka[GetOrgEmployeesUseCase],
        gpt_tarologue: FromDishka[IGPTTarologue]
) -> CompareListSchema:
    user = await get_user.execute(GetUserQuery(user_id=user_id))
    employees = await get_employees.execute(GetOrgEmployeesQuery(org_id=current_org.id))

    analyses = []
    for employee in employees:
        analysis = await gpt_tarologue.compare_analyze(user=user, boss=employee.user)
        analyses.append(CompareAnalyzeSchema.from_entity(analysis))
    best_employee = analyses[0]
    best_score = best_employee.compatibility.score
    for analysis in analyses:
        if analysis.compatibility.score > best_score:
            best_score = analysis.compatibility.score
            best_employee = analysis
    analyses.remove(best_employee)
    result = {
        "best_match": best_employee,
        'other_matches': analyses
    }
    return result


@router.post(
    path="/atmosphere",
    summary="Оценка атмосферы в команде по таро",
    operation_id="atmosphereTaro",
    response_model=AtmosphereAnalyzeSchema
)
async def compare_user_boss_taro(
        current_org: CurrentOrgDep,
        get_employees: FromDishka[GetOrgEmployeesUseCase],
        gpt_tarologue: FromDishka[IGPTTarologue]
) -> AtmosphereAnalyzeSchema:
    employees = await get_employees.execute(GetOrgEmployeesQuery(org_id=current_org.id))
    analyze = await gpt_tarologue.atmosphere_analyze(users=[employee.user for employee in employees])

    return AtmosphereAnalyzeSchema.from_entity(analyze)
