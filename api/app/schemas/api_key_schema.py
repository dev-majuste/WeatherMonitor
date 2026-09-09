from pydantic import BaseModel


class ApiKeyCreateSchema(BaseModel):
    name: str
    key: str | None = None
    requests_per_minute: int = 30


class ApiKeyUpdateSchema(BaseModel):
    name: str | None = None
    active: bool | None = None
    requests_per_minute: int | None = None


class ApiKeyResponseSchema(BaseModel):
    id: int
    name: str
    key: str
    active: bool
    requests_per_minute: int

    class Config:
        from_attributes = True