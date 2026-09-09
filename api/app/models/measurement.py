from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

def brazil_time():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[float] = mapped_column(Float, nullable=False)
    pressure: Mapped[float] = mapped_column(Float, nullable=False)
    raindrop: Mapped[int] = mapped_column(Integer, nullable=False)
    luminosity: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=brazil_time,
        nullable=False
    )