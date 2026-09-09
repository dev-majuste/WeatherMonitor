from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import DEVICE_API_KEY, ADMIN_API_KEY
from app.database.connection import get_db
from app.repositories.api_key_repository import ApiKeyRepository
from app.services.rate_limit_service import RateLimitService


def validate_device_key(
    x_device_key: str = Header(...)
):
    if x_device_key != DEVICE_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid device key"
        )


def validate_admin_key(
    x_admin_key: str = Header(...)
):
    if x_admin_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin key"
        )


def validate_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    api_key = ApiKeyRepository.get_by_key(
        db,
        x_api_key
    )

    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    if not api_key.active:
        raise HTTPException(
            status_code=403,
            detail="API key disabled"
        )

    if not RateLimitService.check(
        api_key.key,
        api_key.requests_per_minute
    ):
        raise HTTPException(
            status_code=429,
            detail="Request limit exceeded"
        )

    return api_key