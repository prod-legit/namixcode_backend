from pydantic import BaseModel


class StatusSchema(BaseModel):
    status: bool
    message: str
