from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.database.database import Base

from app.models.measurement import Measurement
import app.models.api_key

from app.routes.measurement_route import router as measurement_router
from app.routes.api_key_route import router as api_key_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(measurement_router)
app.include_router(api_key_router)