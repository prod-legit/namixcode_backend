from dishka import Provider, provide, Scope

from app.logic.commands.apply.create_apply import CreateApplyUseCase
from app.logic.commands.auth.decode_jwt import DecodeJWTUseCase
from app.logic.commands.auth.generate_jwt import GenerateJWTUseCase
from app.logic.commands.org.create_org import CreateOrgUseCase
from app.logic.commands.user.create_user import CreateUserUseCase
from app.logic.queries.apply.get_org_applies import GetOrgAppliesUseCase
from app.logic.queries.apply.get_user_applies import GetUserAppliesUseCase
from app.logic.queries.org.get_org import GetOrgUseCase
from app.logic.queries.org.get_orgs import GetOrgsUseCase
from app.logic.queries.user.get_user import GetUserUseCase
from app.settings import Settings


class LogicProvider(Provider):
    create_apply_use_case = provide(CreateApplyUseCase, scope=Scope.REQUEST)

    create_org_use_case = provide(CreateOrgUseCase, scope=Scope.REQUEST)
    get_org_use_case = provide(GetOrgUseCase, scope=Scope.REQUEST)
    get_orgs_use_case = provide(GetOrgsUseCase, scope=Scope.REQUEST)

    create_user_use_case = provide(CreateUserUseCase, scope=Scope.REQUEST)
    get_user_use_case = provide(GetUserUseCase, scope=Scope.REQUEST)

    get_org_applies_use_case = provide(GetOrgAppliesUseCase, scope=Scope.REQUEST)
    get_user_applies_use_case = provide(GetUserAppliesUseCase, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def generate_jwt_user_case(self, settings: Settings) -> GenerateJWTUseCase:
        return GenerateJWTUseCase(
            secret=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

    @provide(scope=Scope.APP)
    def validate_jwt_user_case(self, settings: Settings) -> DecodeJWTUseCase:
        return DecodeJWTUseCase(
            secret=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
