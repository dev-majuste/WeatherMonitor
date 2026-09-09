from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.api_key import ApiKey


class ApiKeyRepository:

    @staticmethod
    def create(db: Session, api_key: ApiKey):
        db.add(api_key)
        db.commit()
        db.refresh(api_key)

        return api_key

    @staticmethod
    def get_all(db: Session):
        statement = select(ApiKey).order_by(
            ApiKey.id.asc()
        )

        return db.scalars(statement).all()

    @staticmethod
    def get_by_id(
        db: Session,
        api_key_id: int
    ):
        statement = select(ApiKey).where(
            ApiKey.id == api_key_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_key(
        db: Session,
        key: str
    ):
        statement = select(ApiKey).where(
            ApiKey.key == key
        )

        return db.scalar(statement)

    @staticmethod
    def update(db: Session, api_key: ApiKey):
        db.commit()
        db.refresh(api_key)

        return api_key