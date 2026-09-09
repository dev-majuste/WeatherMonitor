from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.auth_service import validate_admin_key
from app.database.connection import get_db
from app.schemas.api_key_schema import (
    ApiKeyCreateSchema,
    ApiKeyUpdateSchema,
    ApiKeyResponseSchema
)
from app.services.api_key_service import ApiKeyService


router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"],
    dependencies=[Depends(validate_admin_key)]
)


@router.post(
    "",
    response_model=ApiKeyResponseSchema,
    status_code=201
)
def create_api_key(
    data: ApiKeyCreateSchema,
    db: Session = Depends(get_db)
):
    return ApiKeyService.create(db, data)


@router.get(
    "",
    response_model=list[ApiKeyResponseSchema]
)
def get_api_keys(
    db: Session = Depends(get_db)
):
    return ApiKeyService.get_all(db)


@router.get(
    "/{api_key_id}",
    response_model=ApiKeyResponseSchema
)
def get_api_key(
    api_key_id: int,
    db: Session = Depends(get_db)
):
    api_key = ApiKeyService.get_by_id(
        db,
        api_key_id
    )

    if api_key is None:
        raise HTTPException(
            status_code=404,
            detail="API key not found"
        )

    return api_key


@router.patch(
    "/{api_key_id}",
    response_model=ApiKeyResponseSchema
)
def update_api_key(
    api_key_id: int,
    data: ApiKeyUpdateSchema,
    db: Session = Depends(get_db)
):
    api_key = ApiKeyService.update(
        db,
        api_key_id,
        data
    )

    if api_key is None:
        raise HTTPException(
            status_code=404,
            detail="API key not found"
        )

    return api_key