from sqlalchemy import Boolean, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[float] = mapped_column(Float, nullable=False)
    pressure: Mapped[float] = mapped_column(Float, nullable=False)
    raindrop: Mapped[int] = mapped_column(Integer, nullable=False)
    luminosity: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[str] = mapped_column(nullable=False)