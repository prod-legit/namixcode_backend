from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path
from pydantic import UUID4

from app.application.api.dependencies import CurrentUserDep, CurrentOrgDep
from app.application.api.schemas.analyze import AnalyzeSchema
from app.application.api.schemas.apply import ApplySchema, CreateApplySchema
from app.infrastructure.services.gpt_tarologue import IGPTTarologue
from app.logic.commands.apply.create_apply import CreateApplyUseCase, CreateApplyCommand
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
        org_id=str(data.org_id),
        user_id=current_user.id
    ))

    return ApplySchema.from_entity(apply)


@router.get(
    path="/{user_id}",
    summary="Получить анализ пользователя по таро",
    operation_id="analyzeUserTaro",
    response_model=AnalyzeSchema
)
async def analyze_user_taro(
        current_org: CurrentOrgDep,
        user_id: Annotated[UUID4, Path()],
        get_user: FromDishka[GetUserUseCase],
        gpt_tarologue: FromDishka[IGPTTarologue]
) -> AnalyzeSchema:
    user = await get_user.execute(GetUserQuery(user_id=user_id))
    analyze = await gpt_tarologue.analyze(user)

    return AnalyzeSchema.from_entity(analyze)
