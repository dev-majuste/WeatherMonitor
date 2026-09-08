
from fastapi import APIRouter


router = APIRouter(prefrix="/measurements", tags=["measurements"])

#esp32 post
@router.post("", status_code=201)
def create_measurement():
    pass

#users get latest measurement
@router.get("/latest", status_code=200)
def get_latest_measurement():
    pass

#user get day measurements
@router.get("/day", status_code=200)
def get_day_measurements():
    pass

#user get week measurements
@router.get("/week", status_code=200)
def get_week_measurements():
    pass

#user get month measurements
@router.get("/month", status_code=200)
def get_month_measurements():
    pass