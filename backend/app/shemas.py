from pydantic import BaseModel
from typing import List, Optional

class PanelConfig(BaseModel):
    latitude: float = 43.30
    longitude: float = 5.37
    power_kwc: float = 3.0
    surface_m2: float = 20.0
    orientation: float = 180.0
    tilt: float = 30.0
    efficiency: float = 0.20

class DayPrediction(BaseModel):
    date: str
    production_kwh: float
    irradiance: float
    temperature: float
    cloud_cover: float
    economies_eur: float
    co2_evite_kg: float

class PredictionResponse(BaseModel):
    location: str
    total_production_kwh: float
    total_economies_eur: float
    total_co2_evite_kg: float
    predictions: List[DayPrediction]