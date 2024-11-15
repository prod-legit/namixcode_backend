from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.dependencies import CurrentUserDep
from app.application.api.schemas.auth import AuthToken
from app.application.api.schemas.user import CreateUserSchema, UserSchema
from app.logic.commands.auth.generate_jwt import GenerateJWTUseCase, GenerateJWTCommand
from app.logic.commands.user.create_user import CreateUserUseCase, CreateUserCommand

router = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute
)


@router.post(
    path="/register",
    summary="Регистрация пользователя",
    operation_id="regUser",
    status_code=201,
    response_model=AuthToken
)
async def register_user(
        data: CreateUserSchema,
        create_user: FromDishka[CreateUserUseCase],
        generate_jwt: FromDishka[GenerateJWTUseCase]
) -> AuthToken:
    user = await create_user.execute(CreateUserCommand(
        email=data.email,
        password=data.password,
        name=data.name,
        phone=data.phone,
        experience=data.experience,
        skills=data.skills,
        interests=data.interests
    ))
    token = await generate_jwt.execute(GenerateJWTCommand(sub=user.id))

    return AuthToken(token=token)


@router.get(
    path="/me",
    summary="Получить текущего пользователя",
    operation_id="getCurrentUser",
    response_model=UserSchema
)
async def get_current_user(current_user: CurrentUserDep) -> UserSchema:
    return UserSchema.from_entity(current_user)
