import secrets

from sqlalchemy.orm import Session

from app.models.api_key import ApiKey
from app.repositories.api_key_repository import ApiKeyRepository
from app.schemas.api_key_schema import (
    ApiKeyCreateSchema,
    ApiKeyUpdateSchema
)


class ApiKeyService:

    @staticmethod
    def create(
        db: Session,
        data: ApiKeyCreateSchema
    ):
        api_key = ApiKey(
            name=data.name,
            key=data.key if data.key else secrets.token_hex(8),
            requests_per_minute=data.requests_per_minute,
            active=True
        )

        return ApiKeyRepository.create(
            db,
            api_key
        )

    @staticmethod
    def get_all(db: Session):
        return ApiKeyRepository.get_all(db)

    @staticmethod
    def get_by_id(
        db: Session,
        api_key_id: int
    ):
        return ApiKeyRepository.get_by_id(
            db,
            api_key_id
        )

    @staticmethod
    def get_by_key(
        db: Session,
        key: str
    ):
        return ApiKeyRepository.get_by_key(
            db,
            key
        )

    @staticmethod
    def update(
        db: Session,
        api_key_id: int,
        data: ApiKeyUpdateSchema
    ):
        api_key = ApiKeyRepository.get_by_id(
            db,
            api_key_id
        )

        if api_key is None:
            return None

        if data.name is not None:
            api_key.name = data.name

        if data.active is not None:
            api_key.active = data.active

        if data.requests_per_minute is not None:
            api_key.requests_per_minute = data.requests_per_minute

        return ApiKeyRepository.update(
            db,
            api_key
        )