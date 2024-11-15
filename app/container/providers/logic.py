from dishka import Provider, provide, Scope

from app.logic.commands.apply.create_apply import CreateApplyUseCase


class LogicProvider(Provider):
    create_apply_use_case = provide(CreateApplyUseCase, scope=Scope.REQUEST)
