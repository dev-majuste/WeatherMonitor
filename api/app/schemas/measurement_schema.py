from pydantic import BaseModel
from datetime import datetime

class MeasurementCreateSchema(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    luminosity: int
    raindrop: int


class MeasurementResponseSchema(BaseModel):
    id: int
    temperature: float
    humidity: float
    pressure: float
    luminosity: int
    raindrop: int
    timestamp: datetime

    class Config:
        from_attributes = True