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
       correction_temp = 1 + coeff_temp * (temp - 25)
       correction_temp =  max(0.7, min(1.1, correction_temp))
       correction_nuages = 1 - (cloud_cover / 100) * 0.60
       correction_nuages = max(0.2, correction_nuages)
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

    model = XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42)
    model.fit(x, y)
    return model 

def predict_next_7_days(model,df:pd.DataFrame,config) -> list:
   """Prédit les 7 prochains jours en se basant sur les données historiques similaires"""   
   predictions = []
   today = datetime.now()

   for i in range(1,8):
        target_date = today + timedelta(days=i)
        day_of_year = target_date.timetuple().tm_yday
        month = target_date.month

        # Prendre la moyenne des mêmes jours les années précédentes

        similar = df[(df["day_of_year"].between(day_of_year -7, day_of_year +7)) & (df["month"] == month)]
        if similar.empty:
             similar = df[df["month"] == month]
        
        irradiance = float(similar["irradiance"].mean())
        temperature = float(similar["temperature"].mean())
        cloud_cover = float(similar["cloud_cover"].mean())
        wind_speed = float(similar["wind_speed"].mean())

        # Formule physique = base
        base_production = compute_production(irradiance, temperature, cloud_cover, config)

        # XGBoost ajuste selon patterns historiques
        features = np.array([[irradiance, temperature, cloud_cover, wind_speed, day_of_year, month]])
        xgb_output = float(model.predict(features)[0])

        correction_factor = xgb_output / (base_production + 0.001)
        correction_factor = max(0.85, min(1.15, correction_factor))

        production = base_production * correction_factor
        predictions.append({
            "date": target_date.strftime("%Y-%m-%d"),
            "production_kwh": round(production, 2),
            "irradiance": round(irradiance, 2),
            "temperature": round(temperature, 1),
            "cloud_cover": round(cloud_cover, 1),
            "economies_eur": round(production * PRIX_KWH, 2),
            "co2_evite_kg": round(production * CO2_KWH, 2),
        })
    
   return predictions