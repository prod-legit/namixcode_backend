from pydantic import BaseModel


class StatusSchema(BaseModel):
    status: bool
    message: str

    @classmethod
    def success(cls, message: str = "success") -> "StatusSchema":
        return cls(status=True, message=message)

    @classmethod
    def error(cls, message: str = "error") -> "StatusSchema":
        return cls(status=False, message=message)
