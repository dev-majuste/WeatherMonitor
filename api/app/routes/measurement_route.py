from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.measurement_schema import (
    MeasurementCreateSchema,
    MeasurementResponseSchema
)
from app.services.auth_service import (
    validate_api_key,
    validate_device_key
)
from app.services.measurement_service import MeasurementService


router = APIRouter(
    prefix="/measurements",
    tags=["Measurements"]
)


@router.post(
    "",
    response_model=MeasurementResponseSchema,
    status_code=201,
    dependencies=[Depends(validate_device_key)]
)
def create_measurement(
    data: MeasurementCreateSchema,
    db: Session = Depends(get_db)
):
    return MeasurementService.create(db, data)


@router.get(
    "/latest",
    response_model=MeasurementResponseSchema,
    dependencies=[Depends(validate_api_key)]
)
def get_latest_measurement(
    db: Session = Depends(get_db)
):
    measurement = MeasurementService.get_latest(db)

    if measurement is None:
        raise HTTPException(
            status_code=404,
            detail="Measurement not found"
        )

    return measurement


@router.get(
    "/day",
    response_model=list[MeasurementResponseSchema],
    dependencies=[Depends(validate_api_key)]
)
def get_measurements_day(
    date_value: date | None = Query(
        default=None,
        alias="date"
    ),
    db: Session = Depends(get_db)
):
    return MeasurementService.get_day(
        db,
        date_value
    )


@router.get(
    "/week",
    response_model=list[MeasurementResponseSchema],
    dependencies=[Depends(validate_api_key)]
)
def get_measurements_week(
    db: Session = Depends(get_db)
):
    return MeasurementService.get_week(db)


@router.get(
    "/month",
    response_model=list[MeasurementResponseSchema],
    dependencies=[Depends(validate_api_key)]
)
def get_measurements_month(
    month: int | None = Query(
        default=None,
        ge=1,
        le=12
    ),
    year: int | None = Query(
        default=None,
        ge=2000
    ),
    db: Session = Depends(get_db)
):
    return MeasurementService.get_month(
        db,
        month,
        year
    )