from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.shemas import PanelConfig, PredictionResponse
from app.nasa import fetch_nasa_data
from app.openmeteo import fetch_forcast
from app.model import train_model, predict_from_forecast

app = FastAPI(title="SolarCast API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "SolarCast API running 🌞"}



@app.post("/predict", response_model=PredictionResponse)
async def predict(config: PanelConfig):
    try:
        # 1. NASA — 40 ans d'historique pour entraîner XGBoost
        nasa_df = await fetch_nasa_data(config.latitude, config.longitude)

        # 2. Entraîne XGBoost sur l'historique NASA
        model = train_model(nasa_df, config)

        # 3. Open-Meteo — vraies prévisions météo 7 prochains jours
        forecast_df = fetch_forcast(config.latitude, config.longitude)

        # 4. XGBoost prédit la production sur les vraies prévisions
        predictions = predict_from_forecast(model, forecast_df, config)

        total_production = sum(p["production_kwh"] for p in predictions)
        total_economies = sum(p["economies_eur"] for p in predictions)
        total_co2 = sum(p["co2_evite_kg"] for p in predictions)

        return PredictionResponse(
            location=f"{config.latitude}, {config.longitude}",
            total_production_kwh=round(total_production, 2),
            total_economies_eur=round(total_economies, 2),
            total_co2_evite_kg=round(total_co2, 2),
            predictions=predictions
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/health")
def health():
    return {"status": "ok"}