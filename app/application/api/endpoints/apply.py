from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.schemas.apply import ApplySchema, CreateApplySchema
from app.logic.commands.apply.create_apply import CreateApplyUseCase, CreateApplyCommand

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
        data: CreateApplySchema,
        create_apply: FromDishka[CreateApplyUseCase]
) -> ApplySchema:
    apply = await create_apply.execute(CreateApplyCommand(
        name=data.name,
        phone=data.phone,
        email=data.email,
        experience=data.experience,
        skills=data.skills,
        interests=data.interests
    ))

    return ApplySchema.from_entity(apply)
