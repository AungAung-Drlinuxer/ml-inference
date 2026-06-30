"""
ml-inference / app / main.py

Minimal FastAPI inference endpoint for fraud detection.
Features passed as ordered list of floats.

Endpoints:
  GET  /health   — liveness probe
  GET  /ready    — readiness probe (checks model loaded)
  POST /predict  — run inference, returns label + confidence + latency
"""

import os
import time
import uuid
import joblib
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from monitor import InferenceMonitor

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
model = None
monitor = InferenceMonitor()

# ---------------------------------------------------------------------------
# Application lifecycle
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model_path = os.getenv("MODEL_PATH", "/app/model/model.pkl")
    try:
        model = joblib.load(model_path)
        print(f"[OK] Model loaded: {model_path}")
    except Exception as e:
        print(f"[CRITICAL] Model loading failed: {e}")
    yield
    print("[OK] Shutting down server context.")


app = FastAPI(
    title="ML Inference API",
    version=os.getenv("MODEL_VERSION", "1.0.0"),
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class PredictRequest(BaseModel):
    features:     List[float]
    labels:       Optional[List[str]] = None
    ground_truth: Optional[int] = None


class PredictResponse(BaseModel):
    request_id:    str
    label:         str
    label_index:   int
    confidence:    float
    probabilities: List[float]
    latency_ms:    float


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}


@app.get("/ready")
def ready():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready"}


@app.post("/predict", response_model=PredictResponse)
async def predict(request: Request, body: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not ready")

    t_start = time.perf_counter()

    # ---- 1. Preprocessing ----
    t_pre = time.perf_counter()
    X = np.array(body.features).reshape(1, -1)
    preprocessing_ms = (time.perf_counter() - t_pre) * 1000

    # ---- 2. Inference ----
    t_inf = time.perf_counter()
    label_index = int(model.predict(X)[0])
    probs = model.predict_proba(X)[0].tolist()
    inference_ms = (time.perf_counter() - t_inf) * 1000

    # ---- 3. Postprocessing ----
    t_post = time.perf_counter()
    labels = body.labels or [str(i) for i in range(len(probs))]
    label = labels[label_index] if label_index < len(labels) else str(label_index)
    postprocessing_ms = (time.perf_counter() - t_post) * 1000

    total_ms = (time.perf_counter() - t_start) * 1000

    # ---- 4. Telemetry (fire-and-forget) ----
    monitor.log_inference(
        input_features={"features": body.features},
        prediction_label=label,
        prediction_index=label_index,
        probabilities=probs,
        latency_ms=total_ms,
        preprocessing_ms=preprocessing_ms,
        inference_ms=inference_ms,
        postprocessing_ms=postprocessing_ms,
        client_ip=request.client.host if request.client else "unknown",
    )

    return PredictResponse(
        request_id=str(uuid.uuid4()),
        label=label,
        label_index=label_index,
        confidence=round(max(probs), 4),
        probabilities=[round(p, 4) for p in probs],
        latency_ms=round(total_ms, 3),
    )
