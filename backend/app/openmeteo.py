import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta


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
    cloud_cover = daily.Variables(3).ValuesAsNumpy()
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
        "cloud_cover": cloud_cover,
        "wind_speed": wind_speed,
    })

    df["day_of_year"] = df["date"].dt.dayofyear
    df["month"] = df["date"].dt.month

    return df