import requests
import pandas as pd
import math
from datetime import datetime

def fetch_forcast(lat: float, lon: float) -> pd.DataFrame:
    API_KEY = "DWZU4BL96B8HLMJF7YQA9Z7GW"
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/next7days?unitGroup=metric&elements=datetime,solarradiation,tempmax,tempmin,windspeed&include=days&key={API_KEY}&contentType=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Erreur: {e}")
        return pd.DataFrame()

    forecast_data = []
    for day in data['days']:
        irradiance_kwh = (day.get('solarradiation', 0) * 24) / 1000

        forecast_data.append({
            "date": pd.to_datetime(day['datetime']),
            "irradiance": irradiance_kwh,
            "temp_max": day.get('tempmax', 0),
            "temp_min": day.get('tempmin', 0),
            "wind_speed": day.get('windspeed', 0)
        })

    df = pd.DataFrame(forecast_data)
    df["temperature"] = (df["temp_max"] + df["temp_min"]) / 2
    df["day_of_year"] = df["date"].dt.dayofyear
    df["month"] = df["date"].dt.month

    df["cloud_cover"] = df.apply(
        lambda row: calculate_effective_cloud_cover(row["irradiance"], lat, row["day_of_year"]),
        axis=1
    )

    df = df[["date", "irradiance", "temperature", "wind_speed", "day_of_year", "month", "cloud_cover"]]
    return df

def calculate_effective_cloud_cover(irradiance:float, latitude:float, date_of_year:int) -> float:
    max_iradiance = 7.5 
    mid_year = 172 
    amplitude = 2.25
    moyenne = 6.25

    seasonal_factor = math.cos(2 * math.pi * (date_of_year - mid_year) / 365)
    theoritical_max = moyenne + (amplitude * seasonal_factor)
    
    ratio = min(irradiance / theoritical_max, 1.0) if theoritical_max > 0 else 0
    effective_cloud = max(0, (1 - ratio) * 100)

    return round(effective_cloud, 1)