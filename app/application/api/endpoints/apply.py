from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.dependencies import CurrentUserDep
from app.application.api.schemas.apply import ApplySchema, CreateApplySchema
from app.logic.commands.apply.create_apply import CreateApplyUseCase, CreateApplyCommand
from app.logic.queries.apply.get_user_applies import GetUserAppliesUseCase, GetUserAppliesQuery

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
    path="/my",
    summary="Получить отклики текущего пользователя",
    operation_id="getCurrentUserApplies",
    response_model=list[ApplySchema]
)
async def get_current_user_applies(
        current_user: CurrentUserDep,
        get_user_applies: FromDishka[GetUserAppliesUseCase]
) -> list[ApplySchema]:
    applies = await get_user_applies.execute(GetUserAppliesQuery(user_id=current_user.id))
    return [ApplySchema.from_entity(apply) for apply in applies]
