from calendar import monthrange
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.repositories.measurement_repository import MeasurementRepository
from app.schemas.measurement_schema import MeasurementCreateSchema
from app.services.cache_service import CacheService


BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")


class MeasurementService:

    @staticmethod
    def create(
        db: Session,
        data: MeasurementCreateSchema
    ):
        measurement = Measurement(
            temperature=data.temperature,
            humidity=data.humidity,
            pressure=data.pressure,
            luminosity=data.luminosity,
            raindrop=data.raindrop
        )

        measurement = MeasurementRepository.create(
            db,
            measurement
        )

        CacheService.clear()

        return measurement

    @staticmethod
    def get_latest(db: Session):
        cached = CacheService.get("latest")

        if cached is not None:
            return cached

        measurement = MeasurementRepository.get_latest(db)

        CacheService.set(
            "latest",
            measurement
        )

        return measurement

    @staticmethod
    def get_day(
        db: Session,
        selected_date: date | None = None
    ):
        if selected_date is None:
            selected_date = datetime.now(BRAZIL_TZ).date()

        cache_key = f"day:{selected_date}"

        cached = CacheService.get(cache_key)

        if cached is not None:
            return cached

        start = datetime.combine(
            selected_date,
            time.min
        )

        end = datetime.combine(
            selected_date,
            time.max
        )

        measurements = MeasurementRepository.get_between(
            db,
            start,
            end
        )

        CacheService.set(
            cache_key,
            measurements
        )

        return measurements

    @staticmethod
    def get_week(db: Session):
        now = datetime.now(BRAZIL_TZ)

        cache_key = f"week:{now.date()}"

        cached = CacheService.get(cache_key)

        if cached is not None:
            return cached

        start = now - timedelta(days=7)

        measurements = MeasurementRepository.get_between(
            db,
            start,
            now
        )

        CacheService.set(
            cache_key,
            measurements
        )

        return measurements

    @staticmethod
    def get_month(
        db: Session,
        month: int | None = None,
        year: int | None = None
    ):
        now = datetime.now(BRAZIL_TZ)

        if month is None and year is None:
            cache_key = f"last30:{now.date()}"

            cached = CacheService.get(cache_key)

            if cached is not None:
                return cached

            start = now - timedelta(days=30)

            measurements = MeasurementRepository.get_between(
                db,
                start,
                now
            )

            CacheService.set(
                cache_key,
                measurements
            )

            return measurements

        if month is None:
            month = now.month

        if year is None:
            year = now.year

        cache_key = f"month:{year}:{month}"

        cached = CacheService.get(cache_key)

        if cached is not None:
            return cached

        last_day = monthrange(
            year,
            month
        )[1]

        start = datetime(
            year,
            month,
            1
        )

        end = datetime(
            year,
            month,
            last_day,
            23,
            59,
            59
        )

        measurements = MeasurementRepository.get_between(
            db,
            start,
            end
        )

        CacheService.set(
            cache_key,
            measurements
        )

        return measurements