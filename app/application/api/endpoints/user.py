from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.api.dependencies import CurrentUserDep
from app.application.api.schemas.apply import ApplySchema
from app.application.api.schemas.auth import AuthToken
from app.application.api.schemas.employee import EmployeeSchema
from app.application.api.schemas.user import CreateUserSchema, UserSchema, LoginUserSchema
from app.logic.commands.auth.generate_jwt import GenerateJWTUseCase, GenerateJWTCommand
from app.logic.commands.user.create_user import CreateUserUseCase, CreateUserCommand
from app.logic.queries.apply.get_user_applies import GetUserAppliesUseCase, GetUserAppliesQuery
from app.logic.queries.employee.get_user_employments import GetUserEmploymentsUseCase, GetUserEmploymentsQuery
from app.logic.queries.user.get_user_auth import GetUserAuthUseCase, GetUserAuthQuery

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
        sex=data.sex,
        birthdate=data.birthdate,
        experience=data.experience,
        professions=data.professions,
        interests=data.interests
    ))
    token = await generate_jwt.execute(GenerateJWTCommand(sub=user.id))

    return AuthToken(token=token)


@router.post(
    path="/login",
    summary="Вход пользователя",
    operation_id="loginUser",
    response_model=AuthToken
)
async def login_user(
        data: LoginUserSchema,
        auth_user: FromDishka[GetUserAuthUseCase],
        generate_jwt: FromDishka[GenerateJWTUseCase]
) -> AuthToken:
    user = await auth_user.execute(GetUserAuthQuery(
        email=data.email,
        password=data.password
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


@router.get(
    path="/applies",
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


@router.get(
    path="/employments",
    summary="Получить работодателей",
    operation_id="listUserEmployments",
    response_model=list[EmployeeSchema]
)
async def get_current_user_employments(
        current_user: CurrentUserDep,
        get_employments: FromDishka[GetUserEmploymentsUseCase]
) -> list[EmployeeSchema]:
    employments = await get_employments.execute(GetUserEmploymentsQuery(current_user.id))
    return [EmployeeSchema.from_entity(employment) for employment in employments]
