from pydantic import BaseModel


class AuthToken(BaseModel):
    token: str
    type: str = "Bearer"
