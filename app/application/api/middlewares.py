from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse
from app.application.api.schemas.status import StatusSchema
from app.domain.exceptions.base import AppException
from app.logic.exceptions.auth import AuthException
from app.logic.exceptions.base import (
    AccessForbiddenException,
    ObjectExistsException,
    ObjectNotFoundException,
)


def get_http_code(exc: AppException) -> int:
    if isinstance(exc, ObjectNotFoundException):
        return status.HTTP_404_NOT_FOUND
    elif isinstance(exc, ObjectExistsException):
        return status.HTTP_409_CONFLICT
    elif isinstance(exc, AccessForbiddenException):
        return status.HTTP_403_FORBIDDEN
    elif isinstance(exc, AuthException):
        return status.HTTP_401_UNAUTHORIZED
    return status.HTTP_400_BAD_REQUEST


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except AppException as exc:
            code = get_http_code(exc)
            response_schema = StatusSchema(status=False, message=str(exc))
            data = jsonable_encoder(response_schema)
            return JSONResponse(status_code=code, content=data)
