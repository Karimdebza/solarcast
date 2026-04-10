import httpx
from datetime import datetime, timedelta
import pandas as pd


NASA_BASE = "https://power.larc.nasa.gov/api/temporal/daily/point"

async def fetch_nasa_data(lat:float,lon:float,days_nack:int = 365) -> pd.DataFrame:
    end = datetime.now() - timedelta(days=7)
    start = end - timedelta(days=days_nack)

    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M,CLOUD_AMT,WS10M",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start.strftime("%Y%m%d"),
        "end": end.strftime("%Y%m%d"),
        "format": "JSON"
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response =  await client.get(NASA_BASE, params=params)
    response.raise_for_status()
    data = response.json()

    props = data["properties"]["parameter"]
    dates = list(props["ALLSKY_SFC_SW_DWN"].keys())
    df = pd.DataFrame({
        "date": pd.to_datetime(dates, format="%Y%m%d"),
        "irradiance": list(props["ALLSKY_SFC_SW_DWN"].values()),
        "temperature": list(props["T2M"].values()),
        "cloud_cover": list(props["CLOUD_AMT"].values()),
        "wind_speed": list(props["WS10M"].values()),
    })

    df = df[df["irradiance"] > 0]

    df["day_of_year"] = df["date"].dt.dayofyear
    df["month"] = df["date"].dt.month

    return df

