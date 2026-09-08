from pydantic import BaseModel

class MeasurementCreateSchema(BaseModel):
    temperature: float
    humidity: float
    pressure: float
    luminosity: int
    raindrop: bool

class MeasurementResponse(BaseModel):
    id: int
    temperature: float
    humidity: float
    pressure: float
    luminosity: int
    raindrop: bool
    date: str