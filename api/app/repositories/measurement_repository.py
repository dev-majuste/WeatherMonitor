from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.measurement import Measurement


class MeasurementRepository:

    @staticmethod
    def create(db: Session, measurement: Measurement):
        db.add(measurement)
        db.commit()
        db.refresh(measurement)

        return measurement

    @staticmethod
    def get_latest(db: Session):
        statement = (
            select(Measurement)
            .order_by(Measurement.timestamp.desc())
            .limit(1)
        )

        return db.scalar(statement)

    @staticmethod
    def get_between(
        db: Session,
        start: datetime,
        end: datetime
    ):
        statement = (
            select(Measurement)
            .where(
                Measurement.timestamp >= start,
                Measurement.timestamp <= end
            )
            .order_by(Measurement.timestamp.asc())
        )

        return db.scalars(statement).all()