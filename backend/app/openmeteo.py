import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta
import math 

def fetch_forcast(lat: float, lon: float) -> pd.DataFrame:
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "shortwave_radiation_sum",
            "temperature_2m_max",
            "temperature_2m_min",
            "cloud_cover_mean",
            "wind_speed_10m_max"
        ],
        "timezone": "auto",
        "forecast_days": 7
    }

    responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]
    daily = response.Daily()

    irradiance = daily.Variables(0).ValuesAsNumpy()
    temp_max = daily.Variables(1).ValuesAsNumpy()
    temp_min = daily.Variables(2).ValuesAsNumpy()
#
    wind_speed = daily.Variables(4).ValuesAsNumpy()

    dates = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        periods=len(irradiance),
        freq="D"
    )

    df = pd.DataFrame({
        "date": dates,
        "irradiance": irradiance / 3.6,
        "temperature": (temp_max + temp_min) / 2,
        "wind_speed": wind_speed,
    })

    df["day_of_year"] = df["date"].dt.dayofyear
    df["month"] = df["date"].dt.month

    df["cloud_cover"] = df.apply(
            lambda row: calculate_effective_cloud_cover(row["irradiance"], lat, row["day_of_year"]),
            axis=1
        )

    print("FORECAST AVEC CLOUD COVER CALCULÉ:", df)
    return df


def calculate_effective_cloud_cover(irradiance:float, latitude:float, date_of_year:int) -> float:
    """Calcule une estimation du cloud cover effectif basé sur l'irradiance, la latitude et le jour de l'année."""
    # Formule empirique : plus l'irradiance est faible que prévu pour la saison, plus le cloud cover effectif est élevé
    # Au printemps (avril), le max réel est proche de 7.2 kWh/m²/j
    # En été (juin), il monte à 8.5 kWh/m²/j
    # On peut utiliser 7.5 comme base plus réaliste pour avril
    max_iradiance = 7.5 # kWh/m²/jour, valeur typique pour un jour d'été en plein soleil
    # ratio = min(irradiance / max_iradiance, 1.0)
    mid_year = 172 
    amplitude = 2.25
    moyenne =  6.25


    seasonal_factor = math.cos(2 * math.pi * (date_of_year - mid_year) / 365)

    theoritical_max =  moyenne + (amplitude * seasonal_factor)

    ratio  =  min(irradiance /  theoritical_max, 1.0)

    effective_cloud = max(0, (1 - ratio) * 100)

    return round(effective_cloud, 1)