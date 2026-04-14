import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

PRIX_KWH = 0.2062
CO2_KWH = 0.055
PERFORMANCE_RATIO = 0.80

def compute_production(irradiance: float, temp: float, cloud_cover: float, config) -> float:
       """Formule physique : P = irradiance × surface × rendement × correction_temp"""
       coeff_temp = -0.004 # -0.4% par °C au dessus de 25°C
       temp_cellule = temp + (irradiance * 20 / 0.8)
       correction_temp = 1 + coeff_temp * (temp_cellule - 25)
       
       correction_temp =  max(0.6, min(1.0, correction_temp))
       correction_nuages = 1 - (cloud_cover / 100) * 0.25
    #    correction_nuages = max(0.2, correction_nuages)
       # Formule : Pkwc × (irradiance/peak_irradiance) × PR × correction_temp
       production = config.power_kwc * irradiance * PERFORMANCE_RATIO * correction_temp * correction_nuages
       return round(max(0, production), 3)

def train_model(df:pd.DataFrame, config):
    """Entraîne XGBoost sur les données historiques NASA"""
    df = df.copy()
    df["production"] = df.apply(lambda row: compute_production(row["irradiance"],  row["temperature"], row["cloud_cover"], config), axis=1)
    features = ["irradiance", "temperature", "cloud_cover", "wind_speed", "day_of_year", "month"]
    x = df[features].values
    y = df["production"].values

    model = XGBRegressor(n_estimators=300, max_depth=5, learning_rate=0.05,subsample=0.8, random_state=42)
    model.fit(x, y)
    return model 

def predict_from_forecast(model: XGBRegressor, forecast_df: pd.DataFrame, config) -> list:
   """
   Prédit la production à partir des VRAIES prévisions Open-Meteo.
   XGBoost apprend les patterns NASA → prédit sur météo réelle future.
   """
   predictions = []
   today = datetime.now()

   for _, row in forecast_df.iterrows():
        features = np.array([[
            row["irradiance"],
            row["temperature"],
            row["cloud_cover"],
            row["wind_speed"],
            row["day_of_year"],
            row["month"]
        ]])
        production = float(model.predict(features)[0])
        production = max(0, production)


        predictions.append({
            "date": row["date"].strftime("%Y-%m-%d"),
            "production_kwh": round(production, 2),
            "irradiance": round(row["irradiance"], 2),
            "temperature": round(row["temperature"], 1),
            "cloud_cover": round(row["cloud_cover"], 1),
            "economies_eur": round(production * PRIX_KWH, 2),
            "co2_evite_kg": round(production * CO2_KWH, 2),
        })
    
   return predictions