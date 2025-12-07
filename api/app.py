from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow.pyfunc
import os

# --- Ajout pour Prometheus ---
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI(title="Air Quality API", description="API de prédiction AQI binaire")

# ==========================
# Chargement du modèle
# ==========================
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model")
FEATURE_NAMES_PATH = os.path.join(BASE_DIR, "model", "feature_names.txt")

model = mlflow.pyfunc.load_model(MODEL_PATH)

if os.path.exists(FEATURE_NAMES_PATH):
    with open(FEATURE_NAMES_PATH, "r", encoding="utf-8") as f:
        FEATURE_COLUMNS = f.read().split(",")
else:
    FEATURE_COLUMNS = None

# ==========================
# Schéma de la requête
# ==========================
class FeaturesInput(BaseModel):
    features: dict

# ==========================
# Metrics Prometheus
# ==========================
TOTAL_REQUESTS = Counter("total_requests", "Total number of API requests")
TOTAL_PREDICTIONS = Counter("total_predictions", "Total number of predictions made")
LAST_PREDICTION_STATUS = Gauge("last_prediction_status", "Last prediction status (0=bad,1=good)")
LAST_PREDICTION_LATENCY_MS = Gauge("last_prediction_latency_ms", "Latency of last prediction in ms")
AVG_PREDICTION_LATENCY_MS = Gauge("avg_prediction_latency_ms", "Average prediction latency in ms")

# Pour calculer la moyenne des latences
latencies = []

# ==========================
# Endpoints
# ==========================
@app.get("/")
def home():
    return {"message": "API Air Quality opérationnelle."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
def predict(request: FeaturesInput):
    import time
    TOTAL_REQUESTS.inc()
    start = time.time()

    if FEATURE_COLUMNS is None:
        return {"error": "feature_names.txt introuvable. Relancer select_best.py."}

    data = {col: 0.0 for col in FEATURE_COLUMNS}
    for key, value in request.features.items():
        if key in data:
            data[key] = value

    df = pd.DataFrame([data])
    pred = model.predict(df)[0]

    latency_ms = (time.time() - start) * 1000
    latencies.append(latency_ms)
    LAST_PREDICTION_LATENCY_MS.set(latency_ms)
    AVG_PREDICTION_LATENCY_MS.set(sum(latencies) / len(latencies))
    LAST_PREDICTION_STATUS.set(pred)
    TOTAL_PREDICTIONS.inc()

    return {
        "prediction": int(pred),
        "details": {
            "input_used": request.features,
            "nb_features_total": len(FEATURE_COLUMNS)
        }
    }
