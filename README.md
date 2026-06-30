# ML Inference Service — Production-Grade Fraud Detection

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.2-orange)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.12.0-yellow)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 📑 မာတိကာ (Table of Contents)

1. [Project Overview — ပရောဂျက်အကြောင်း ခြုံငုံသုံးသပ်ချက်](#1-project-overview)
2. [Architecture — ဗိသုကာပုံစံ](#2-architecture)
3. [File-by-File Deep Dive — ဖိုင်တစ်ဖိုင်ချင်းစီ၏ အသေးစိတ်ရှင်းလင်းချက်](#3-file-by-file-deep-dive)
   - [3.1 `app/main.py` — Inference Server](#31-appmainpy--inference-server)
   - [3.2 `app/monitor.py` — Elasticsearch Logger](#32-appmonitorpy--elasticsearch-logger)
   - [3.3 `app/collect_metrics.py` — Metrics Collector](#33-appcollect_metrics.py--metrics-collector)
   - [3.4 `app/train_model.py` — Model Training](#34-apptrain_modelpy--model-training)
   - [3.5 `app/requirements.txt` — Dependencies](#35-apprequirementstxt--dependencies)
   - [3.6 `app/__init__.py` — Package Marker](#36-app__init__py--package-marker)
   - [3.7 `Dockerfile` — Container Build](#37-dockerfile--container-build)
   - [3.8 `model/model.pkl` — Trained Model](#38-modelmodelpkl--trained-model)
4. [Setup Instructions — တပ်ဆင်နည်း](#4-setup-instructions)
5. [API Documentation](#5-api-documentation)
6. [Elasticsearch Integration — ES ချိတ်ဆက်မှု](#6-elasticsearch-integration)
7. [Security Best Practices — လုံခြုံရေးအကြံပြုချက်များ](#7-security-best-practices)
8. [Production Deployment Guide](#8-production-deployment-guide)
9. [Troubleshooting — အမှားရှာဖွေခြင်း](#9-troubleshooting)
10. [Roadmap — ဆက်လက်ဆောင်ရွက်ရန်](#10-roadmap)

---

## 1. Project Overview — ပရောဂျက်အကြောင်း ခြုံငုံသုံးသပ်ချက်

### 1.1 ဒီ Project က ဘာလဲ? (What is this project?)

ဒီ Project သည် **Machine Learning Model** (Fraud Detection) တစ်ခုကို **Production-grade REST API** အဖြစ် အသုံးပြုနိုင်ရန် တည်ဆောက်ထားသော **MLOps Inference Service** ဖြစ်ပါသည်။

ဆိုလိုသည်မှာ — ကျွန်ုပ်တို့တွင် ငွေလိမ်မှု (Fraud) ကို ရှာဖွေနိုင်သော Model တစ်ခုရှိပြီး၊ ၎င်းကို HTTP Request များမှတစ်ဆင့် ခေါ်ယူအသုံးပြုနိုင်ရန် API အနေဖြင့် ထုတ်ပေးထားခြင်းဖြစ်သည်။

### 1.2 ဘယ်လိုအလုပ်လုပ်လဲ? (How does it work?)

```
Client (curl / App / Website)
        │
        ▼
  ┌─────────────────┐
  │  FastAPI Server  │  ← port 8080
  │  (main.py)       │
  └────────┬────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  ┌──────┐  ┌──────────┐
  │Model │  │   ES     │
  │.pkl  │  │Monitor   │
  └──────┘  └────┬─────┘
                 ▼
          ┌──────────────┐
          │Elasticsearch │
          │192.168.1.123 │
          │:80 (HAProxy) │
          └──────────────┘
```

**Flow အဆင့်ဆင့်:**

1. Client က `POST /predict` သို့ features (ငွေပမာဏ၊ လက်ကျန်ငွေစသည်) များကို JSON အဖြစ်ပို့သည်
2. FastAPI Server က features များကို numpy array အဖြစ်ပြောင်းသည် (Preprocessing)
3. Model (`model.pkl`) က prediction လုပ်သည် — ငွေလိမ်မှုရှိ/မရှိ ခန့်မှန်းသည် (Inference)
4. Prediction result ကို JSON response အဖြစ် Client သို့ပြန်ပို့သည် (Postprocessing)
5. တစ်ချိန်တည်းမှာပင် Inference Log ကို Elasticsearch သို့ အလိုအလျောက်ပို့သည် (Monitoring)
6. နောက်ခံမှ `collect_metrics.py` က ၁၅ မိနစ်တစ်ခါ ES မှ log များကိုယူကာ Performance Metrics (accuracy, F1, latency) များကိုတွက်သည်

### 1.4 ဘယ်လိုနည်းပညာတွေ သုံးထားလဲ? (Tech Stack)

| Technology | Version | အသုံးပြုပုံ |
|-----------|---------|-------------|
| **Python** | 3.11+ | Programming language |
| **FastAPI** | 0.111 | REST API framework (async support, auto-docs) |
| **uvicorn** | 0.30 | ASGI server (FastAPI ကို run ပေးတယ်) |
| **scikit-learn** | 1.4.2 | ML model training + inference |
| **GradientBoostingClassifier** | — | Fraud detection model (ensemble of decision trees) |
| **Elasticsearch** | 8.12.0 (client) / 8.19.17 (server) | Log storage + metrics + drift detection |
| **Prometheus Instrumentator** | 6.1.0 | `/metrics` endpoint အတွက် |
| **evidently** | 0.4.30 | Data drift detection |
| **Docker** | — | Containerization |
| **pydantic** | 2.7.0 | Data validation (request/response schema) |
| **joblib** | 1.4.2 | Model serialization (save/load .pkl) |

### 1.5 Project Structure — ဖိုင်တည်ဆောက်ပုံ

```
ml-inference/
│
├── app/                           # Application code (Python package)
│   ├── __init__.py                # Package marker (ဒါရှိမှ Python package အဖြစ်အလုပ်လုပ်)
│   ├── main.py                    # ★ FastAPI Server (entry point, endpoints)
│   ├── monitor.py                 # ★ ES logging class (inference + metrics + drift)
│   ├── collect_metrics.py         # ★ Background metrics collector (cron-friendly)
│   ├── train_model.py             # Model training script (one-time run)
│   └── requirements.txt           # Python dependencies
│
├── Dockerfile                     # Container build instruction (multi-stage)
│
├── model/
│   └── model.pkl                  # Trained model artifact (GradientBoosting)
│
├── data/
│   ├── sample_data.csv            # 10,000 synthetic fraud rows
│   └── reference.csv              # 1,000 baseline for drift detection
│
├── README.md                      # ဒီ file (project documentation)
├── lab.md                         # Lab exercises များ
└── solution.md                    # Lab solutions များ
```

---

## 2. Architecture — ဗိသုကာပုံစံ

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client / End User                           │
│              (curl, mobile app, website, microservice)              │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ HTTP POST /predict
                            │ {"features": [250.0, 5000.0, ...]}
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     HAProxy / Load Balancer                         │
│                       (port 80 → 8080)                              │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│              ┌─────────────────────────────────────┐               │
│              │       FastAPI Inference Server      │               │
│              │         (uvicorn + main.py)         │               │
│              │            port 8080                │               │
│              ├─────────────────────────────────────┤               │
│              │                                     │               │
│              │  ┌──────────┐   ┌────────────────┐  │               │
│              │  │  Model   │   │  Inference      │  │               │
│              │  │  Engine  │   │  Monitor        │  │               │
│              │  │ (joblib) │   │ (ES Logging)    │  │               │
│              │  └────┬─────┘   └───────┬────────┘  │               │
│              │       │                 │           │               │
│              └───────┼─────────────────┼───────────┘               │
│                      │                 │                           │
│                      ▼                 ▼                           │
│              ┌──────────────┐  ┌──────────────┐                    │
│              │   model/     │  │    ES Host   │                    │
│              │   model.pkl  │  │  192.168.1.123:80                │
│              └──────────────┘  └──────┬───────┘                   │
│                                       │                           │
└───────────────────────────────────────┼───────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     Elasticsearch 8.19.17                    │  │
│  │                        (3 nodes)                            │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │                                                              │  │
│  │  ┌─────────────────────┐  ┌─────────────────────┐           │  │
│  │  │  ml-inference index │  │  ml-metrics index   │           │  │
│  │  │  (per-request logs) │  │  (aggregated perf)  │           │  │
│  │  ├─────────────────────┤  ├─────────────────────┤           │  │
│  │  │ @timestamp          │  │ @timestamp          │           │  │
│  │  │ request_id          │  │ model_name          │           │  │
│  │  │ model_name          │  │ model_version       │           │  │
│  │  │ input_features      │  │ performance.accuracy│           │  │
│  │  │ prediction.label    │  │ performance.f1      │           │  │
│  │  │ prediction.confidence│  │ performance.p95    │           │  │
│  │  │ performance.latency │  │ drift.drift_detected│           │  │
│  │  │ status              │  │ window_minutes      │           │  │
│  │  └─────────────────────┘  └─────────────────────┘           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

                         Background Process:
┌─────────────────────────────────────────────────────────────────────┐
│  collect_metrics.py (sidecar / cron)                               │
│                                                                     │
│  Every 15 minutes:                                                  │
│    1. Fetch recent predictions from ES ml-inference index           │
│    2. Compute accuracy, precision, recall, F1, latency p95/p99      │
│    3. Save results to ES ml-metrics index                           │
│    4. Run data-drift detection (Evidently)                          │
│    5. Log drift results to ES ml-metrics index                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Request Lifecycle — Request တစ်ခုရဲ့ ဘဝစက်ဝန်း

အောက်ပါ diagram က `POST /predict` request တစ်ခု ဘယ်လိုအလုပ်လုပ်သွားလဲဆိုတာကို အချိန်ကာလအလိုက်ပြထားသည်:

```
Time (ms)
│
├─ 0.000 ── Client က POST /predict ပို့သည်
│           Request Body: {"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}
│
├─ 0.012 ── Preprocessing (0.012ms)
│           ├─ JSON deserialization (pydantic)
│           ├─ List[float] → numpy array
│           └─ reshape(1, -1) → shape (1, 5)
│
├─ 0.723 ── Inference (0.711ms)
│           ├─ model.predict(X) → label_index: 0
│           ├─ model.predict_proba(X) → [0.99999999, 7.39e-9]
│           ├─ label: "0" (not fraud)
│           └─ confidence: 1.0 (99.999999%)
│
├─ 0.725 ── Postprocessing (0.002ms)
│           ├─ label_index → label string
│           └─ Build response JSON
│
├─ 0.725 ── Response ပြန်ပို့သည်
│           Response: {"label": "0", "confidence": 1.0, ...}
│
├─ 0.773 ── Telemetry (0.048ms) — ES သို့ log ရေးသည် (fire-and-forget)
│           ├─ ES host: 192.168.1.123:80
│           ├─ Index: ml-inference
│           └─ Status: 201 Created
│
└─ 0.773 ── Request အဆုံး
└─ 0.773 ── Request အဆုံး

---

## 3. File-by-File Deep Dive — ဖိုင်တစ်ဖိုင်ချင်းစီ၏ အသေးစိတ်ရှင်းလင်းချက်

ဒီအခန်းမှာ project ထဲက file တစ်ခုချင်းစီရဲ့ ဘယ်လိုအလုပ်လုပ်လဲဆိုတာကို
အသေးစိတ်ရှင်းပြထားပါတယ်။ Code ရဲ့ line တစ်ကြောင်းချင်းစီရဲ့
အဓိပ္ပါယ်နဲ့ ဘာကြောင့်ဒီလိုရေးထားလဲဆိုတာကိုပါ ဖော်ပြပေးထားပါတယ်။

---

### 3.1 `app/main.py` — Inference Server

**Location:** `ml-inference/app/main.py`
**Purpose:** FastAPI REST API server — model loading, prediction endpoint, health checks
**Dependencies:** FastAPI, uvicorn, numpy, joblib, monitor.py
**Lines:** ~132

#### 3.1.1 File Overview (ဖိုင်အကြောင်းအကျဉ်း)

`main.py` သည် project ၏ **entry point** ဖြစ်သည်။ ၎င်းသည်:

1. Server startup မှာ model.pkl ကို memory ထဲသို့ load လုပ်သည်
2. InferenceMonitor (ES logger) ကို initialize လုပ်သည်
3. REST API endpoints ၃ ခုကို expose လုပ်သည်:
   - `GET /health` — Liveness probe (server အသက်ရှိ/မရှိ)
   - `GET /ready` — Readiness probe (server က traffic လက်ခံနိုင်/မနိုင်)
   - `POST /predict` — Model inference
4. Request တစ်ခုချင်းစီအတွက် latency breakdown တွက်သည်
5. Inference log ကို Elasticsearch သို့ပို့သည်

#### 3.1.2 Code Breakdown (Line-by-Line)

```python
"""
ml-inference / app / main.py

Minimal FastAPI inference endpoint for fraud detection.
Features passed as ordered list of floats.

Endpoints:
  GET  /health   — liveness probe
  GET  /ready    — readiness probe (checks model loaded)
  POST /predict  — run inference, returns label + confidence + latency
"""
```

**Docstring:** ဖိုင်ရဲ့ထိပ်ဆုံးမှာရှိတဲ့ comment block က documentation ဖြစ်တယ်။
ဒီဖိုင်က ဘာလဲ၊ endpoint တွေက ဘာတွေလဲဆိုတာကို ဖော်ပြထားတယ်။
Python docstring convention အရ """...""" ကို သုံးထားတယ်။

```python
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
```

**Imports များ၏ ရှင်းလင်းချက်:**

| Library | အသုံးပြုပုံ | ဘာကြောင့်လိုအပ်လဲ |
|---------|-------------|-------------------|
| `os` | Environment variable ဖတ်ရန် | MODEL_PATH, ES_HOST etc. |
| `time` | Latency တိုင်းရန် | `time.perf_counter()` — high precision timer |
| `uuid` | Request ID တစ်ခုစီအတွက် | Unique ID for traceability |
| `joblib` | Model .pkl ဖိုင်ကို load ရန် | Faster than pickle for numpy arrays |
| `numpy` | Feature array ပြောင်းရန် | `np.array(body.features).reshape(1, -1)` |
| `asynccontextmanager` | Server startup/shutdown စီမံရန် | FastAPI lifespan pattern |
| `FastAPI` | REST API framework | Auto-docs, validation, async support |
| `Request` | Client IP ရယူရန် | `request.client.host` |
| `HTTPException` | Error response ပြန်ရန် | 503 Model not loaded, etc. |
| `BaseModel` | Request/Response schema | pydantic data validation |
| `InferenceMonitor` | ES logging class | monitor.py မှ import လုပ် |

```python
# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
model = None
monitor = InferenceMonitor()
```

**Global Variables:**

- `model`: Model object ကို သိမ်းဆည်းရန်။ Server startup မှာ load လုပ်ပြီး ဒီ variable ထဲထည့်တယ်။
  `None` ဖြစ်နေရင် model မရှိသေးဘူးလို့ဆိုလိုတယ်။
  
- `monitor`: InferenceMonitor ၏ instance တစ်ခု။ Module level မှာ တစ်ခါပဲ initialize လုပ်တယ်။
  ES ကို log ရေးဖို့ သုံးတယ်။

**Note:** ဒါက Singleton pattern ပဲ။
Traditional app မှာ database connection pool တစ်ခုကို application startup မှာ initialize
လုပ်ပြီး တစ်နေရာတည်းကနေ ပြန်သုံးသလိုပဲ — ဒီမှာလည်း ES client connection pool ကို
တစ်ခါပဲဆောက်ပြီး request တိုင်းအတွက် ပြန်သုံးတယ်။

```python
# ---------------------------------------------------------------------------
# Application lifecycle
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown logic."""
    global model
    model_path = os.getenv("MODEL_PATH", "/app/model/model.pkl")
    try:
        model = joblib.load(model_path)
        print(f"[OK] Model loaded: {model_path}")
    except Exception as e:
        print(f"[CRITICAL] Model loading failed: {e}")
    yield
    print("[OK] Shutting down server context.")
```

**Lifespan Handler ရှင်းလင်းချက်:**

`@asynccontextmanager` decorator က FastAPI ကို ဒီ function က startup/shutdown logic ရှိတယ်လို့ပြောတယ်။

**Startup Phase (before `yield`):**

1. `global model` — module-level model variable ကို ပြောင်းလို့ရအောင်ကြေညာတယ်
2. `os.getenv("MODEL_PATH", "/app/model/model.pkl")` — Environment variable ကနေ model path ကိုဖတ်တယ်။
   မရှိရင် default `/app/model/model.pkl` ကိုသုံးတယ် (Docker runtime အတွက်)
3. `joblib.load(model_path)` — model.pkl ဖိုင်ကို memory ထဲ load လုပ်တယ်
4. `try/except` — Model load မရရင် error print ထုတ်ပြီး server က continue လုပ်တယ်
   (model မပါဘဲ start ဖြစ်သွားပေမယ့် predict endpoint က 503 return ပြန်မယ်)

**Shutdown Phase (after `yield`):**

- Server ကို stop လုပ်တဲ့အခါ "Shutting down server context." ဆိုတဲ့ message ကိုပြပြီး
  cleanup လုပ်တယ်။ (ဒီ project မှာ cleanup လုပ်စရာသိပ်မရှိဘူး — model variable က
  Python garbage collector ကြည့်မယ်)

**Note:** ဒါက preStop hook နဲ့ဆင်တယ်။
Container ကိုမသတ်ခင် cleanup လုပ်ဖို့ signal ပေးတာပဲ။

```python
app = FastAPI(
    title="ML Inference API",
    version=os.getenv("MODEL_VERSION", "1.0.0"),
    lifespan=lifespan,
)
```

**FastAPI App Creation:**

- `title`: Swagger UI မှာပြမယ့် title
- `version`: Environment variable ကနေဖတ်တယ်။ မရှိရင် "1.0.0"
- `lifespan`: အထက်မှာ define လုပ်ထားတဲ့ lifespan function

FastAPI က auto-generate လုပ်ပေးတဲ့ `/docs` (Swagger UI) နဲ့ `/redoc` တွေကိုပါ
အလိုအလျောက် expose လုပ်ပေးတယ် — ဒါက FastAPI ရဲ့အားသာချက်ပဲ။

```python
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
```

**Pydantic Models ရှင်းလင်းချက်:**

**PredictRequest** (Request Body Schema):

| Field | Type | Required | ရှင်းလင်းချက် |
|-------|------|----------|----------------|
| `features` | `List[float]` | ✅ | Model input value ၅ ခု (ငွေပမာဏ, မူလပိုင်ရှင်လက်ကျန်, ...) |
| `labels` | `Optional[List[str]]` | ❌ | Class name mapping (eg. ["not_fraud", "fraud"]) |
| `ground_truth` | `Optional[int]` | ❌ | Future feedback loop အတွက် |

**PredictResponse** (Response Body Schema):

| Field | Type | ရှင်းလင်းချက် |
|-------|------|----------------|
| `request_id` | `str` | UUID v4 — log tracing အတွက် |
| `label` | `str` | Human-readable class name ("0" or "1") |
| `label_index` | `int` | Numeric class index (0 or 1) |
| `confidence` | `float` | Max probability (0.0 to 1.0) |
| `probabilities` | `List[float]` | All class probabilities |
| `latency_ms` | `float` | End-to-end latency in milliseconds |

**📌 Note:** Pydantic က TypeScript/Java က DTO (Data Transfer Object)
တို့နဲ့ဆင်တယ်။ Request/Response ရဲ့ shape ကို define လုပ်ပြီး validation ကို
auto-matically လုပ်ပေးတယ်။ FastAPI က OpenAPI spec ကိုပါ auto-generate လုပ်ပေးတယ်။

```python
# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}
```

**GET /health — Liveness Probe:**

- Liveness probe အတွက် endpoint
- `model_loaded` field က model ရှိ/မရှိ boolean ပြန်တယ်
- Model မရှိရင်တောင် 200 OK ပြန်တယ် (server က alive ဖြစ်နေတုန်း)

```python
@app.get("/ready")
def ready():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready"}
```

**GET /ready — Readiness Probe:**

- Readiness probe အတွက် endpoint
- Model မရှိရင် **503 Service Unavailable** return ပြန်တယ်
- ဒါက "server က traffic မလက်ခံနိုင်သေးဘူး" လို့ပြောတာပဲ
- Model load မအောင်ရင် traffic ကို အခြား instances တွေဆီပဲပို့မယ်

```python
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
```

**POST /predict — Main Inference Endpoint:**

ဒီ endpoint က project ရဲ့ core ဖြစ်တယ်။ အဆင့် ၄ ဆင့်ခွဲထားတယ်:

**Step 1: Preprocessing (0.012ms)**
```python
t_pre = time.perf_counter()
X = np.array(body.features).reshape(1, -1)
preprocessing_ms = (time.perf_counter() - t_pre) * 1000
```

- `body.features` က `[250.0, 5000.0, 4750.0, 2000.0, 2250.0]` (List[float])
- `np.array(...)` က numpy array အဖြစ်ပြောင်းတယ် → `array([250., 5000., ...])`
- `.reshape(1, -1)` က shape ကို `(1, 5)` အဖြစ်ပြောင်းတယ်
  - `1` = batch size (row ၁ ခု)
  - `5` = feature အရေအတွက်
- scikit-learn model က 2D array လိုအပ်တယ် — `(n_samples, n_features)`
- `time.perf_counter()` က high-precision timer — nanoseconds အထိတိုင်းတယ်

**Step 2: Inference (0.711ms)**
```python
t_inf = time.perf_counter()
label_index = int(model.predict(X)[0])
probs = model.predict_proba(X)[0].tolist()
inference_ms = (time.perf_counter() - t_inf) * 1000
```

- `model.predict(X)` → `array([0])` (class 0 = not fraud)
  - XGBoost/LightGBM လိုမဟုတ်ဘဲ scikit-learn က 2D array လိုအပ်တယ်
  - Output က 1D array — `[0]` for single sample
  - `[0]` နဲ့ scalar ကိုထုတ်ယူ → `int()` နဲ့ integer ပြောင်း
- `model.predict_proba(X)` → `array([[0.99999999, 7.39e-9]])`
  - Row 1 က sample တစ်ခု
  - Column 0 က class 0 probability (not fraud: 99.999999%)
  - Column 1 က class 1 probability (fraud: 0.0000007%)
  - `[0]` နဲ့ first row ကိုယူ → `.tolist()` နဲ့ Python list ပြောင်း

**📌 ML Theory:** GradientBoosting က decision tree တွေကို sequential ဆက်ကာ
ensemble လုပ်တယ်။ Tree တစ်ခုချင်းစီက previous tree ရဲ့ error ကို
ပြင်ဆင်တယ် (boosting). ဒါက random forest (parallel trees) နဲ့မတူဘူး။

**Step 3: Postprocessing (0.002ms)**
```python
t_post = time.perf_counter()
labels = body.labels or [str(i) for i in range(len(probs))]
label = labels[label_index] if label_index < len(labels) else str(label_index)
postprocessing_ms = (time.perf_counter() - t_post) * 1000
```

- `body.labels or [str(i) for i in range(len(probs))]`:
  - Client က labels မပို့ရင် default labels ထုတ်တယ် — `["0", "1"]`
  - `len(probs)` = 2 (classes 2 ခု)
  - List comprehension: `[str(0), str(1)]`
- `label = labels[label_index]`:
  - label_index = 0 → label = "0" (not fraud)
  - label_index = 1 → label = "1" (fraud)
- Fallback: `if label_index < len(labels)` — index out of range မဖြစ်အောင်

**Step 4: Telemetry (0.048ms)**
```python
monitor.log_inference(
    input_features={"features": body.features},
    prediction_label=label,
    prediction_index=label_index,
    probabilities=probs,
    latency_ms=total_ms,
    ...
)
```

- Fire-and-forget pattern — ES write က response ကိုမမြန်အောင်မလုပ်ဘူး
- monitor.log_inference() ထဲမှာ try/except နဲ့ ဖမ်းထားတယ်
- ES down သွားရင်လည်း predict endpoint က ဆက်အလုပ်လုပ်တယ်

**Response:**
```python
return PredictResponse(
    request_id=str(uuid.uuid4()),
    label=label,
    label_index=label_index,
    confidence=round(max(probs), 4),
    probabilities=[round(p, 4) for p in probs],
    latency_ms=round(total_ms, 3),
)
```

- `uuid.uuid4()` က random UUID v4 ထုတ်တယ် — log tracing အတွက်
- `round(max(probs), 4)` — confidence ကို decimal 4 နေရာအထိလှမ်းတယ်
- `round(total_ms, 3)` — latency ကို decimal 3 နေရာအထိလှမ်းတယ်

---

### 3.2 `app/monitor.py` — Elasticsearch Logger

**Location:** `ml-inference/app/monitor.py`
**Purpose:** ES သို့ inference log, performance metrics, drift report များရေးသော class
**Lines:** ~274

#### 3.2.1 File Overview

`monitor.py` သည် **InferenceMonitor** class တစ်ခုကို define လုပ်ထားတယ်။
ဒီ class က ES နဲ့ချိတ်ဆက်ပြီး အောက်ပါ data အမျိုးအစား ၃ မျိုးကို index လုပ်တယ်:

1. **Inference Logs** (`ml-inference` index) — request တစ်ခုချင်းစီရဲ့ details
2. **Performance Metrics** (`ml-metrics` index) — accuracy, F1, latency percentiles
3. **Drift Reports** (`ml-metrics` index) — data drift detection results

#### 3.2.2 Code Breakdown

```python
import os
import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from typing import Optional
from elasticsearch import Elasticsearch
```

**Imports:**

| Library | ရှင်းလင်းချက် |
|---------|----------------|
| `os` | Environment variable ဖတ်ရန် (ES_HOST, ES_USER, ES_PASS) |
| `uuid` | Request ID generation |
| `numpy` | Array operations (latency percentiles) |
| `pandas` | DataFrame operations (drift detection) |
| `datetime` | Timestamp generation (UTC) |
| `Elasticsearch` | ES client — connection + CRUD operations |

```python
class InferenceMonitor:
    """
    Logs inference requests + aggregated metrics + drift reports
    to Elasticsearch for observability and MLOps auditing.
    """
```

**Class Documentation:**

Docstring က class ရဲ့ purpose ကိုရှင်းပြတယ်။ Sphinx/napoleon style နဲ့
ရေးထားတယ် — auto-documentation tools တွေနဲ့အလုပ်လုပ်တယ်။

```python
def __init__(self):
    es_host = os.getenv("ES_HOST", "http://192.168.1.123:80")
    es_user = os.getenv("ES_USER", "elastic")
    es_pass = os.getenv("ES_PASS", "ML0psElk!2026")

    self.es = Elasticsearch(
        [es_host],
        basic_auth=(es_user, es_pass),
        retry_on_timeout=True,
        max_retries=3,
        request_timeout=10,
    )
    self.inference_index = "ml-inference"
    self.metrics_index = "ml-metrics"
    
    self.model_name = os.getenv("MODEL_NAME", "fraud-detector")
    self.model_version = os.getenv("MODEL_VERSION", "1.0.0")
    self.namespace = os.getenv("NAMESPACE", "ml-inference")
    self.pod_name = os.getenv("POD_NAME", "unknown")
    self.environment = os.getenv("ENVIRONMENT", "production")
```

**Constructor (__init__) ရှင်းလင်းချက်:**

**ES Connection Setup:**
```python
es_host = os.getenv("ES_HOST", "http://192.168.1.123:80")
```

- Environment variable `ES_HOST` ကိုဖတ်တယ်။ မရှိရင် default ကို သုံးတယ်
- **Default: `http://192.168.1.123:80`**
  - Port 80 = HAProxy frontend (သင့် setup အတိုင်း)
  - **Port မပါရင် error တက်တယ်** — elasticsearch-py က URL မှာ scheme, host, port
    ၃ ခုလုံးလိုအပ်တယ်

```python
self.es = Elasticsearch(
    [es_host],
    basic_auth=(es_user, es_pass),
    retry_on_timeout=True,
    max_retries=3,
    request_timeout=10,
)
```

**ES Client Parameters:**

| Parameter | Value | ရှင်းလင်းချက် |
|-----------|-------|----------------|
| First arg | `[es_host]` | List of ES hosts (single node = list of 1) |
| `basic_auth` | `(user, pass)` | HTTP Basic Authentication |
| `retry_on_timeout` | `True` | Timeout ဖြစ်ရင် auto retry |
| `max_retries` | `3` | အများဆုံး retry အကြိမ်ရေ |
| `request_timeout` | `10` | Seconds — request တစ်ခုစီအတွက် timeout |

**📌 Network Note:** ES client 9.x က ES server 8.x နဲ့ မတူဘူး။
9.x client က `Accept: compatible-with=9` header ပို့တယ် — ES 8.19.17 server က
ဒီ header ကို reject လုပ်တယ်။ **ဒါကြောင့် elasticsearch-py 8.12.0 ကိုသုံးထားတယ်။**

```python
self.inference_index = "ml-inference"
self.metrics_index = "ml-metrics"
```

**ES Index Names:**

| Index | Data Type | Retention | Size Estimate (per day) |
|-------|-----------|-----------|------------------------|
| `ml-inference` | Per-request logs | 7-30 days (ILM policy) | ~1KB/doc × 10K req = 10MB |
| `ml-metrics` | Aggregated metrics | 90 days | ~500B/doc × 96 windows = 48KB |

```python
self.model_name = os.getenv("MODEL_NAME", "fraud-detector")
self.model_version = os.getenv("MODEL_VERSION", "1.0.0")
self.namespace = os.getenv("NAMESPACE", "ml-inference")
self.pod_name = os.getenv("POD_NAME", "unknown")
self.environment = os.getenv("ENVIRONMENT", "production")
```

**Deployment Metadata:**

ဒီ field တွေက environment variables ကနေလာတယ်:

```
POD_NAME=$(hostname)
NAMESPACE=$(cat /var/run/secrets/.../namespace)
```

ဒါက ES log ထဲမှာ ဘယ် pod က log ရေးလဲဆိုတာကိုသိဖို့အတွက် — troubleshooting လုပ်ရတာလွယ်တယ်။

```python
def log_inference(self, input_features, prediction_label, prediction_index,
                  probabilities, latency_ms, preprocessing_ms=0.0,
                  inference_ms=0.0, postprocessing_ms=0.0,
                  status="success", error_message=None, client_ip=None):
    ...
    doc = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": str(uuid.uuid4()),
        "model_name": self.model_name,
        "model_version": self.model_version,
        ...
        "input_features": input_features,
        "prediction": {
            "label": prediction_label,
            "label_index": prediction_index,
            "confidence": round(confidence, 4),
            "probabilities": [round(p, 4) for p in probabilities],
        },
        "performance": {
            "latency_ms": round(latency_ms, 3),
            "preprocessing_ms": round(preprocessing_ms, 3),
            "inference_ms": round(inference_ms, 3),
            "postprocessing_ms": round(postprocessing_ms, 3),
        },
        "status": status,
    }
    
    try:
        self.es.index(index=self.inference_index, document=doc)
    except Exception as e:
        print(f"[WARN] ES inference log failed: {e}")
```

**log_inference() Method ရှင်းလင်းချက်:**

ဒီ method က ES `ml-inference` index ထဲသို့ document တစ်စောင်ရေးတယ်။

**Document Structure:**

```
@timestamp:     ISO 8601 UTC timestamp (when the request happened)
request_id:     UUID v4 (for cross-referencing with app logs)
model_name:     Model identifier (for multi-model deployments)
model_version:  Model version (for A/B testing tracking)
pod_name:       Orchestration pod name (for log aggregation)
namespace:      Orchestration namespace (for multi-tenant environments)
environment:    production/staging/development

input_features:
  features:     [250.0, 5000.0, ...]  ← original input

prediction:
  label:        "0" or "1" (human-readable)
  label_index:  0 or 1 (numeric)
  confidence:   0.9999 (max probability)
  probabilities: [0.9999, 0.0001] (per-class)

performance:
  latency_ms:        0.711 (end-to-end)
  preprocessing_ms:  0.012
  inference_ms:      0.697
  postprocessing_ms: 0.002

status:       "success" or "error"
client_ip:    Request origin IP
error_message: (only if status == "error")
```

**Fire-and-Forget Pattern:**
```python
try:
    self.es.index(index=self.inference_index, document=doc)
except Exception as e:
    print(f"[WARN] ES inference log failed: {e}")
```

- ES write က response path ကို မနှောင့်နှေးစေဘူး
- ES down သွားရင်လည်း predict endpoint က ဆက်အလုပ်လုပ်တယ်
- Warning ကို server log ထဲမှာပဲထုတ်တယ် — client ကိုမပြန်ဘူး
- Production မှာ structured logging (structlog / python-json-logger) သုံးသင့်တယ်

```python
def log_performance_metrics(self, y_true, y_pred, y_prob, latencies, window_minutes=15):
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, log_loss
    
    n = len(y_pred)
    if n < 5:
        return
    
    lat = np.array(latencies)
    
    perf = {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, average="weighted", zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, average="weighted", zero_division=0), 4),
        "f1_score": round(f1_score(y_true, y_pred, average="weighted", zero_division=0), 4),
        "log_loss": round(log_loss(y_true, y_prob), 4) if y_prob else None,
        "total_predictions": n,
        "error_count": sum(1 for a, b in zip(y_true, y_pred) if a != b),
        "error_rate": round(sum(1 for a, b in zip(y_true, y_pred) if a != b) / n, 4),
        "avg_latency_ms": round(float(np.mean(lat)), 3),
        "p95_latency_ms": round(float(np.percentile(lat, 95)), 3),
        "p99_latency_ms": round(float(np.percentile(lat, 99)), 3),
    }
    
    doc = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "model_name": self.model_name,
        "model_version": self.model_version,
        "environment": self.environment,
        "window_minutes": window_minutes,
        "performance": perf,
    }
    
    try:
        self.es.index(index=self.metrics_index, document=doc)
    except Exception as e:
        print(f"[WARN] ES metrics log failed: {e}")
```

**log_performance_metrics() Method ရှင်းလင်းချက်:**

ဒီ method က classification metrics တွေကို တွက်ပြီး ES `ml-metrics` index ထဲရေးတယ်။
`collect_metrics.py` ကနေခေါ်တယ် — ၁၅ မိနစ်တစ်ခါ run တယ်။

**Metrics Definitions:**

| Metric | Formula | Range | ရှင်းလင်းချက် |
|--------|---------|-------|----------------|
| **Accuracy** | (TP + TN) / (TP + TN + FP + FN) | 0.0 - 1.0 | မှန်ကန်သော prediction အချိုး |
| **Precision** | TP / (TP + FP) | 0.0 - 1.0 | fraud လို့ပြောတဲ့အထဲက မှန်တဲ့အချိုး |
| **Recall** | TP / (TP + FN) | 0.0 - 1.0 | fraud အကုန်လုံးထဲက ရှာတွေ့တဲ့အချိုး |
| **F1 Score** | 2 × (P × R) / (P + R) | 0.0 - 1.0 | Precision နဲ့ Recall ရဲ့ harmonic mean |
| **Log Loss** | -Σ(y×log(p) + (1-y)×log(1-p)) | 0.0 - ∞ | Probability calibration တိုင်းတာ |

**Why weighted average?**
- `average="weighted"` — class imbalance ကိုထည့်တွက်တယ်။
- Fraud dataset မှာ class 0 (not fraud) က 99.2%, class 1 (fraud) က 0.8%
- "weighted" က 각 class size အလိုက် weight ပေးတယ်
- `zero_division=0` — class တစ်ခုအတွက် prediction မရှိရင် 0 ပြန်တယ် (divide by zero မဖြစ်အောင်)

**Latency Metrics:**

| Metric | ရှင်းလင်းချက် |
|--------|----------------|
| `avg_latency_ms` | Average latency (mean) |
| `p95_latency_ms` | 95th percentile — request 100 ခုမှာ 95 ခုက ဒီထက်မြန်တယ် |
| `p99_latency_ms` | 99th percentile — worst-case latency (excl. outliers) |

**📌 SRE Note:** P95/P99 latency က "tail latency" လို့ခေါ်တယ်။
Average က 1ms ရှိပေမယ့် p99 က 500ms ဆိုရင် user 1% က နှေးတာကိုခံစားရမယ်။
ဒါကြောင့် SLO/SLI အတွက် p99 ကိုအသုံးများတယ်။

```python
def log_drift(self, reference_df, current_df):
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
    
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_df, current_data=current_df)
    result = report.as_dict()
    
    dr = result["metrics"][0]["result"]
    drifted = [
        col for col, val in dr.get("drift_by_columns", {}).items()
        if val.get("drift_detected")
    ]
    
    doc = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "model_name": self.model_name,
        "model_version": self.model_version,
        "environment": self.environment,
        "drift": {
            "data_drift_score": round(dr.get("share_of_drifted_columns", 0.0), 4),
            "drift_detected": dr.get("dataset_drift", False),
            "drifted_features": drifted,
        },
    }
    
    self.es.index(index=self.metrics_index, document=doc)
```

**log_drift() Method ရှင်းလင်းချက်:**

**Data Drift ဆိုတာဘာလဲ?**

Data drift ဆိုတာ production data ရဲ့ distribution က training data နဲ့
ပြောင်းသွားတဲ့အခြေအနေပဲ။ ဥပမာ:

- Training မှာ transaction amount တွေက $10 - $1000 ကြားရှိတယ်
- Production မှာ $5000 - $50000 ကြားတွေများလာတယ်
- Model က ဒီ data အသစ်အတွက် မှန်ကန်တဲ့ prediction မလုပ်နိုင်တော့ဘူး

**Evidently Library ရှင်းလင်းချက်:**

Evidently က open-source ML monitoring library ဖြစ်တယ်။
`DataDriftPreset()` က feature တစ်ခုချင်းစီအတွက်:

1. Numerical features: **Kolmogorov-Smirnov (KS) test** သုံးတယ်
2. Categorical features: **Chi-squared test** သုံးတယ်
3. P-value < 0.05 ဆိုရင် drift ရှိတယ်လို့သတ်မှတ်တယ်
4. `share_of_drifted_columns` က drift ရှိတဲ့ feature အချိုး
5. `dataset_drift` က overall drift flag (`share > 0.3` ဆိုရင် True)

**Drift Detection Workflow:**

```
Training Data (reference)
  ──► 1000 samples from training set
  ──► Column distribution = baseline
  
Production Data (current)
  ──► Last N inference requests
  ──► Same features, different time window
  
Comparison:
  Feature 1: amount
    Train: mean=$500, std=$200
    Prod:  mean=$5000, std=$10000
    KS statistic = 0.45, p-value = 0.001
    → Drift detected! ⚠️
  
  Feature 2: oldbalanceOrg
    Train: mean=$2000, std=$1000
    Prod:  mean=$2000, std=$1200
    KS statistic = 0.02, p-value = 0.89
    → No drift ✅
```

---

### 3.3 `app/collect_metrics.py` — Metrics Collector

**Location:** `ml-inference/app/collect_metrics.py`
**Purpose:** ES မှ inference log များကို အချိန်ကာလအလိုက်ယူကာ metrics တွက်ခြင်း
**Lines:** ~85

#### 3.3.1 File Overview

ဒီ script က **sidecar pattern** အတိုင်းအလုပ်လုပ်တယ် — main server နဲ့
သီးသန့် process တစ်ခုအနေနဲ့ run တယ်။

**Run Modes:**
1. **One-shot:** `python -m app.collect_metrics` (cron job အတွက်)
2. **Loop:** `python -m app.collect_metrics --interval 600` (every 10 min)

#### 3.3.2 Code Breakdown

```python
def fetch_recent_inferences(monitor, minutes=15):
    since = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()
    resp = monitor.es.search(
        index="ml-inference",
        body={
            "query": {
                "bool": {
                    "filter": [
                        {"range": {"@timestamp": {"gte": since}}},
                        {"term": {"status": "success"}},
                    ]
                }
            },
            "size": 10000,
            "_source": [
                "prediction.label_index",
                "prediction.probabilities",
                "performance.latency_ms",
                "input_features",
            ],
        },
    )
    return resp["hits"]["hits"]
```

**ES Query ရှင်းလင်းချက်:**

ဒီ query က လွန်ခဲ့တဲ့ ၁၅ မိနစ်အတွင်းက success status ရှိတဲ့ inference log တွေကိုယူတယ်။

**Query Structure:**
```json
{
  "query": {
    "bool": {
      "filter": [
        {"range": {"@timestamp": {"gte": "2026-06-30T14:00:00+00:00"}}},
        {"term": {"status": "success"}}
      ]
    }
  },
  "size": 10000,
  "_source": ["prediction.label_index", "prediction.probabilities", ...]
}
```

- `bool/filter` — scoring မပါတဲ့ filter query (မြန်တယ်)
- `range` filter — timestamp က ၁၅ မိနစ်အတွင်းဖြစ်ရမယ်
- `term` filter — status က "success" ဖြစ်ရမယ် (failed requests မထည့်ဘူး)
- `size: 10000` — ES default max window
- `_source` — လိုအပ်တဲ့ field တွေပဲပြန်ခိုင်းတယ် (network traffic သက်သာတယ်)

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=0)
    args = parser.parse_args()

    monitor = InferenceMonitor()

    while True:
        hits = fetch_recent_inferences(monitor, minutes=15)
        
        if len(hits) < 5:
            print(f"[SKIP] Only {len(hits)} hits — need ≥ 5 for metrics.")
            ...
            continue
        
        preds = [h["_source"]["prediction"]["label_index"] for h in hits]
        probs = [h["_source"]["prediction"]["probabilities"] for h in hits]
        lats = [h["_source"]["performance"]["latency_ms"] for h in hits]

        monitor.log_performance_metrics(
            y_true=preds, y_pred=preds, y_prob=probs, latencies=lats, window_minutes=15,
        )
        
        # Drift detection
        features = [list(h["_source"]["input_features"]["features"]) for h in hits ...]
        if len(features) >= 20:
            cols = [f"f{i}" for i in range(n_cols)]
            reference = pd.DataFrame(np.random.randn(500, n_cols), columns=cols)
            current = pd.DataFrame(features, columns=cols)
            monitor.log_drift(reference, current)
```

**Main Logic:**

1. ES ကို query လုပ်ပြီး recent inference log တွေယူတယ်
2. Data လုံလောက်မှုစစ်တယ် (≥ 5 samples)
3. Predictions, probabilities, latencies တွေကို list ထဲထည့်တယ်
4. `log_performance_metrics()` ကို call လုပ်တယ်
5. Feature data လုံလောက်ရင် (≥ 20) drift detection လုပ်တယ်
6. Interval mode ဆိုရင် sleep လုပ်ပြီး ပြန် loop တယ်

**📌 Note:** `y_true=preds` — ဒါက **simulated ground truth** ပဲ။
Production မှာ y_true က feedback loop ကနေလာရမယ် (ဥပမာ: user report, manual review)။
ဒါကို နောက်ပိုင်း improvement အတွက်ထားခဲ့တယ်။

---

### 3.4 `app/train_model.py` — Model Training

**Location:** `ml-inference/app/train_model.py`
**Purpose:** Fraud detection model ကို synthetic data နဲ့ train လုပ်ခြင်း
**Lines:** ~100

#### 3.4.1 File Overview

ဒီ script က project ရဲ့ **Model Training Pipeline** ဖြစ်တယ်။
CI/CD pipeline ထဲမှာ ပထမဆုံး run တဲ့ step လို့မြင်နိုင်တယ်။

#### 3.4.2 Code Breakdown

```python
def generate_sample_data(n=10000, seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    
    amount = np.round(np.exp(rng.uniform(1, 10, n)), 2)
    oldbalanceOrg = np.round(amount * rng.uniform(0.5, 5.0, n), 2)
    newbalanceOrig = np.round(oldbalanceOrg - amount * rng.uniform(0.8, 1.2, n), 2)
    oldbalanceDest = np.round(np.exp(rng.uniform(1, 12, n)), 2)
    newbalanceDest = np.round(oldbalanceDest + amount * rng.uniform(0.8, 1.2, n), 2)
    
    is_fraud = np.zeros(n, dtype=int)
    fraud_mask = rng.random(n) < 0.008  # 0.8% fraud rate
    amount[fraud_mask] = np.round(rng.uniform(5000, 50000, n_fraud), 2)
    oldbalanceOrg[fraud_mask] = np.round(rng.uniform(10000, 200000, n_fraud), 2)
    newbalanceOrig[fraud_mask] = 0.0
    is_fraud[fraud_mask] = 1
    
    return pd.DataFrame({...})
```

**Synthetic Data Generation:**

ဒီ function က Kaggle "Synthetic Financial Datasets For Fraud Detection" ကိုအခြေခံတယ်။

**Feature Engineering Logic:**

| Feature | ရှင်းလင်းချက် | Fraud Pattern |
|---------|----------------|---------------|
| `amount` | Transaction ပမာဏ | ပုံမှန် $2.7 - $22,026, Fraud: $5,000 - $50,000 |
| `oldbalanceOrg` | ပေးပို့သူရဲ့မူလလက်ကျန် | Fraud: ပုံမှန်ထက်များတယ် |
| `newbalanceOrig` | ပေးပို့သူရဲ့နောက်ဆုံးလက်ကျန် | Fraud: 0 ဖြစ်တယ် (ငွေအကုန်ထုတ်သွားတယ်) |
| `oldbalanceDest` | လက်ခံသူရဲ့မူလလက်ကျန် | — |
| `newbalanceDest` | လက်ခံသူရဲ့နောက်ဆုံးလက်ကျန် | — |

**Fraud Pattern Injection:**

```python
fraud_mask = rng.random(n) < 0.008
```

Realistic fraud rate: 0.8% (real world: 0.1% - 1%)
Fraud rows မှာ:
- `amount` က $5,000 - $50,000 (ပုံမှန်ထက်များတယ်)
- `oldbalanceOrg` က $10,000 - $200,000
- `newbalanceOrig` က **0.0** (ငွေအကုန်ထုတ်သွားတယ် — fraud indicator)

```python
pipeline = Pipeline([
    ("scaler", RobustScaler()),
    ("classifier", GradientBoostingClassifier(
        n_estimators=150, max_depth=4, learning_rate=0.1,
        subsample=0.8, random_state=42,
    )),
])

pipeline.fit(X_train, y_train)
```

**Pipeline ရှင်းလင်းချက်:**

**RobustScaler:**
- StandardScaler လိုမဟုတ်ဘူး — median နဲ့ IQR ကိုသုံးတယ်
- Outlier တွေကို ခံနိုင်ရည်ရှိတယ်
- Fraud dataset မှာ amount တန်ဖိုးတွေက extreme ဖြစ်တတ်တယ် ($10 နဲ့ $50,000)
- ဒါကြောင့် RobustScaler က StandardScaler ထက်ပိုကောင်းတယ်

**GradientBoostingClassifier:**

| Parameter | Value | ရှင်းလင်းချက် |
|-----------|-------|----------------|
| `n_estimators` | 150 | Decision tree အရေအတွက် |
| `max_depth` | 4 | Tree တစ်ခုချင်းစီရဲ့အနက်ဆုံးအဆင့် |
| `learning_rate` | 0.1 | Tree တစ်ခုချင်းစီရဲ့ contribution ကိုလျှော့ချတယ် |
| `subsample` | 0.8 | Row တွေရဲ့ 80% ကိုပဲသုံးတယ် (random sampling) |
| `random_state` | 42 | Reproducibility အတွက် |

---

### 3.5 `app/requirements.txt` — Dependencies

```text
fastapi==0.111.0
uvicorn[standard]==0.30.0
pydantic==2.7.0
elasticsearch==8.12.0
scikit-learn==1.4.2
numpy==1.26.4
pandas==2.2.2
evidently==0.4.30
joblib==1.4.2
prometheus-fastapi-instrumentator==6.1.0
```

**Package အလိုက်ရှင်းလင်းချက်:**

| Package | Version | Size | ရှင်းလင်းချက် |
|---------|---------|------|----------------|
| `fastapi` | 0.111.0 | ~50KB | REST API framework (async, auto-docs, validation) |
| `uvicorn[standard]` | 0.30.0 | ~200KB | ASGI server (with `standard` extra = httptools, websockets) |
| `pydantic` | 2.7.0 | ~2MB | Data validation via Python type hints |
| `elasticsearch` | 8.12.0 | ~500KB | ES client (v8.x — compatible with ES 8.x server) |
| `scikit-learn` | 1.4.2 | ~15MB | ML algorithms (GradientBoosting, RobustScaler) |
| `numpy` | 1.26.4 | ~60MB | Numerical computing (array operations) |
| `pandas` | 2.2.2 | ~12MB | DataFrame operations (drift detection) |
| `evidently` | 0.4.30 | ~15MB | ML monitoring (drift detection, model evaluation) |
| `joblib` | 1.4.2 | ~200KB | Model serialization (faster than pickle for numpy) |
| `prometheus-fastapi-instrumentator` | 6.1.0 | ~30KB | Auto-generate `/metrics` for Prometheus |

**Version Pinning ရှင်းလင်းချက်:**

Version တွေကို pin ထားတယ် — `==` သုံးထားတယ်။ ဒါက:

- **Reproducible builds** — ဘယ်အချိန် run run တူညီတဲ့ဗားရှင်းတွေရမယ်
- **Security** — မထင်မှတ်တဲ့ breaking changes တွေကိုရှောင်တယ်
- **Audit trail** — ဘယ် version က ဘယ် bug/feature ရှိလဲဆိုတာသိတယ်

**ဘာကြောင့် elasticsearch==8.12.0 လဲ?**

- `8.13.0`: Windows မှာ `opentelemetry` import error တက်တယ်
- `9.x`: ES 8.19.17 server နဲ့မတူဘူး (`Accept: compatible-with=9` header rejected)
- `8.12.0`: Windows မှာအလုပ်လုပ်တယ်၊ ES 8.19.17 နဲ့အဆင်ပြေတယ်

---

### 3.6 `app/__init__.py` — Package Marker

```python
"""ML Inference Service — app package."""
```

ဒီ file က `app/` directory ကို **Python Package** အဖြစ်သတ်မှတ်ပေးတယ်။
ဒါရှိမှ `from app.main import ...` လိုမျိုး import လုပ်လို့ရတယ်။

**📌 Python Note:** Python 3.3+ မှာ `__init__.py` မလိုအပ်တော့ဘူး (namespace packages)
ဒါပေမယ့် project structure ကိုရှင်းရှင်းလင်းလင်းဖြစ်အောင် ထည့်ထားတယ်။

---

### 3.7 `Dockerfile` — Container Build

```dockerfile
# ---- Build stage ----
FROM python:3.11-slim AS builder

WORKDIR /build
COPY app/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgomp1 && \
    pip install --no-cache-dir --user -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# ---- Runtime stage ----
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r inference && useradd -r -g inference -d /app -s /sbin/nologin inference

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY app/ ./
COPY model/ ./model/
RUN mkdir -p /app/model
RUN chown -R inference:inference /app

USER inference

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", \
     "--workers", "2", "--log-level", "info"]
```

**Multi-stage Build ရှင်းလင်းချင်း:**

**Stage 1: Builder**
- `python:3.11-slim` — minimal Python image (Debian-based)
- `build-essential` — C compiler (numpy/scikit-learn compilation အတွက်)
- `libgomp1` — OpenMP library (parallel processing အတွက်)
- `pip install --user` — system ကိုမထိဘဲ user site-packages ထဲ install လုပ်
- `--no-cache-dir` — pip cache မသိမ်းဘူး (image size ချွေတာတယ်)
- Artifacts: `/root/.local` — installed Python packages

**Stage 2: Runtime**
- `python:3.11-slim` — clean image (builder layers မပါ)
- `curl` — HEALTHCHECK အတွက်
- `groupadd / useradd` — non-root user (security best practice)
- `COPY --from=builder` — builder ဆီက packages ကိုပဲယူတယ်
- `USER inference` — root အနေနဲ့ run မထားဘူး

**HEALTHCHECK Parameters:**

| Parameter | Value | ရှင်းလင်းချက် |
|-----------|-------|----------------|
| `--interval` | 30s | ၃၀ စက္ကန့်တစ်ခါစစ်တယ် |
| `--timeout` | 10s | Response စောင့်ချိန် ၁၀ စက္ကန့် |
| `--start-period` | 10s | Startup အတွက် ၁၀ စက္ကန့် grace period |
| `--retries` | 3 | ၃ ကြိမ်ဆက်တိုက်မအောင်ရင် unhealthy |

**uvicorn Parameters:**

| Parameter | Value | ရှင်းလင်းချက် |
|-----------|-------|----------------|
| `--workers` | 2 | Worker processes ၂ ခု (multi-core အတွက်) |
| `--log-level` | info | Default logging level |

---

### 3.8 `model/model.pkl` — Trained Model

**Model Architecture:**
```
Pipeline(steps=[
    ("scaler", RobustScaler()),
    ("classifier", GradientBoostingClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        random_state=42,
    )),
])
```

**Model Performance:**
| Metric | Training | Test |
|--------|----------|------|
| Accuracy | 100% | 100% |

**⚠️ Note:** Synthetic data ဖြစ်တဲ့အတွက် accuracy 100% ရတယ်။
Real-world data အတွက်တော့ ဒီ model က အလုပ်မလုပ်ပါဘူး — 
real transaction data နဲ့ retrain လုပ်ရမယ်။

---

## 4. Setup Instructions — တပ်ဆင်နည်း

### 4.1 Prerequisites (လိုအပ်ချက်များ)

- **Python 3.11+** (3.12 tested)
- **pip** or **uv** (faster package installer)
- **Elasticsearch 8.x** (optional for full features — server can run without ES)
- **Git** (for version control)
- **Docker** (for containerization)

### 4.2 Local Setup

```bash
# 1. Clone
git clone <your-repo-url> ml-inference
cd ml-inference

# 2. Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r app/requirements.txt
# OR with uv (faster):
uv pip install -r app/requirements.txt

# 4. Train model (one-time)
python -m app.train_model

# 5. Run server
cd app
MODEL_PATH=../model/model.pkl \
ES_HOST=http://192.168.1.123:80 \
ES_USER=elastic \
ES_PASS='ML0psElk!2026' \
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# 6. Test
curl http://localhost:8080/health
curl http://localhost:8080/ready

curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
```

### 4.3 Docker Setup

```bash
# 1. Build image
docker build -t ml-inference:latest .

# 2. Run container
docker run -d --name ml-inference \
  -p 8080:8080 \
  -e MODEL_PATH=/app/model/model.pkl \
  -e ES_HOST=http://192.168.1.123:80 \
  -e ES_USER=elastic \
  -e ES_PASS=ML0psElk!2026 \
  ml-inference:latest

# 3. Test
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

---

## 5. API Documentation

### 5.1 Endpoints Summary

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/health` | Liveness probe | None |
| GET | `/ready` | Readiness probe | None |
| POST | `/predict` | Run inference | None (internal network) |

### 5.2 GET /health

**Request:**
```bash
curl http://localhost:8080/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 5.3 GET /ready

**Request:**
```bash
curl http://localhost:8080/ready
```

**Response (200 OK):**
```json
{
  "status": "ready"
}
```

**Response (503 Service Unavailable):**
```json
{
  "detail": "Model not loaded"
}
```

### 5.4 POST /predict

**Request:**
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0],
    "labels": ["not_fraud", "fraud"]
  }'
```

**Response (200 OK):**
```json
{
  "request_id": "a1b2c3d4-...",
  "label": "not_fraud",
  "label_index": 0,
  "confidence": 0.9999,
  "probabilities": [0.9999, 0.0001],
  "latency_ms": 0.711
}
```

**Response (503):**
```json
{
  "detail": "Model not ready"
}
```

---

## 6. Elasticsearch Integration — ES ချိတ်ဆက်မှု

### 6.1 ES Host Setup Checklist

- [ ] ES server 8.x running (8.19.17 confirmed)
- [ ] HAProxy frontend on port 80 → backend :9200
- [ ] `elastic` user with password `ML0psElk!2026`
- [ ] Port 80 accessible from inference server
- [ ] Elasticsearch-py 8.12.0 installed (NOT 9.x)

### 6.2 ES Version Compatibility

```
Client Version    →   Server Version    →   Works?
────────────────────────────────────────────────
8.12.0            →   8.19.17           →   ✅ Yes
8.13.0            →   8.19.17           →   ❌ Windows (opentelemetry)
9.4.1             →   8.19.17           →   ❌ (Accept header mismatch)
```

### 6.3 Indices Structure

```bash
# View all ML indices
curl -u elastic:'ML0psElk!2026' http://192.168.1.123:80/_cat/indices/ml-*?v

# Expected output:
# health status index               docs.count
# green  open   ml-inference-000001  ...
# green  open   ml-metrics-000001    ...
```

---

## 7. Security Best Practices — လုံခြုံရေးအကြံပြုချက်များ

### 7.1 Never Hardcode Secrets

❌ **မလုပ်ရ:**
```python
es_pass = "ML0psElk!2026"  # NEVER hardcode passwords!
```

✅ **လုပ်သင့်:**
```python
es_pass = os.getenv("ES_PASS")
if not es_pass:
    raise ValueError("ES_PASS not set")
```

### 7.2 Environment Variables စီမံခန့်ခွဲခြင်း

**Local development:**
```bash
export ES_PASS='ML0psElk!2026'
```

**Docker:**
```bash
docker run -e ES_PASS=ML0psElk!2026 ...
```

**AWS Secrets Manager:**
```python
import boto3
secrets = boto3.client("secretsmanager")
secret = secrets.get_secret_value(SecretId="ml-inference/es")
```

### 7.3 Production Security Checklist

- [ ] Use **HTTPS** (not HTTP) for ES connection
- [ ] Create **dedicated ES user** (not `elastic` superuser)
- [ ] **Network ACL**: Only inference server IP can reach ES
- [ ] **Firewall**: Block external access to ES port
- [ ] **Secrets rotation**: Change password every 90 days
- [ ] **Audit logging**: Enable ES audit logs
- [ ] **`.gitignore`**: Add `.env`, `*.pem`, `secrets/` to `.gitignore`

---

## 8. Production Deployment Guide

### 8.1 Docker Compose

```yaml
# docker-compose.yml
version: "3.8"
services:
  inference:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MODEL_PATH=/app/model/model.pkl
      - ES_HOST=http://192.168.1.123:80
      - ES_USER=${ES_USER}
      - ES_PASS=${ES_PASS}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  metrics-collector:
    build: .
    command: python -m app.collect_metrics --interval 600
    environment:
      - ES_HOST=http://192.168.1.123:80
      - ES_USER=${ES_USER}
      - ES_PASS=${ES_PASS}
```

---

## 9. Troubleshooting — အမှားရှာဖွေခြင်း

### 9.1 Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'uvicorn'` | Dependencies not installed | `pip install -r app/requirements.txt` |
| `Model not loaded` | model.pkl not found | Check `MODEL_PATH`, run `python -m app.train_model` |
| `ValueError: URL must include a 'scheme', 'host', and 'port'` | ES URL missing port | Use `http://192.168.1.123:80` (with `:80`) |
| `Accept version must be either version 8 or 7, but found 9` | elasticsearch-py 9.x | Install `elasticsearch==8.12.0` |
| `Address already in use` | Port occupied | `taskkill //F //PID <PID>` or change port |
| `[WARN] ES inference log failed` | ES unreachable | Check ES host, credentials, network |

### 9.2 Debug Commands

```bash
# 1. Check ES connectivity
curl -u elastic:'ML0psElk!2026' http://192.168.1.123:80

# 2. Check ES indices
curl -u elastic:'ML0psElk!2026' http://192.168.1.123:80/_cat/indices?v

# 3. Check server logs
docker logs ml-inference

# 4. Check model file exists
ls -la model/model.pkl

# 5. Test model directly
python -c "
import joblib, numpy as np
m = joblib.load('model/model.pkl')
print(m.predict(np.array([[250, 5000, 4750, 2000, 2250]])))
print(m.predict_proba(np.array([[250, 5000, 4750, 2000, 2250]])))
"
```

---

## 10. Roadmap — ဆက်လက်ဆောင်ရွက်ရန်

- [ ] **Real data training** — Replace synthetic data with real transaction data
- [ ] **Model Registry** — SageMaker Model Registry integration
- [ ] **CI/CD Pipeline** — GitHub Actions for auto-train + deploy
- [ ] **A/B Testing** — Multiple model versions serving simultaneously
- [ ] **Feedback Loop** — Ground truth collection from manual reviews
- [ ] **Alerting** — Prometheus + AlertManager for drift/latency alerts
- [ ] **API Gateway** — Rate limiting, authentication, request validation
- [ ] **Multi-model support** — Serve multiple models from one endpoint
- [ ] **Auto-scaling** — Based on request latency
- [ ] **Dashboard** — Grafana dashboard for ML metrics

---

© 2026 ML Inference Service. Built for MLOps learning.

---

## 11. Deep Dive: ML Model Architecture

### 11.1 Gradient Boosting Explained in Detail

Gradient Boosting is an ensemble technique that combines multiple weak learners (decision trees) to create a strong predictor. At step m, the model F_m(x) is updated as:

```
F_m(x) = F_{m-1}(x) + γ_m × h_m(x)
```

Where F_{m-1}(x) is the current ensemble, h_m(x) is a new tree fitting the negative gradient of the loss function, and γ_m is the learning rate. For binary classification, the loss function is log loss:

```
L(y, F(x)) = -[y × log(p) + (1-y) × log(1-p)]
```

#### Training Process

Step 0: F₀(x) = log(odds) = log(fraud_rate / (1 - fraud_rate)) ≈ -4.69 for 0.91% fraud rate. This means the model starts by predicting all transactions as "not fraud" with high probability.

Step 1: Compute residuals r₁ = y - p (difference between true label and predicted probability). Tree 1 fits these residuals, producing h₁(x). Update: F₁(x) = F₀(x) + 0.1 × h₁(x).

Step 2: Compute new residuals from F₁(x). Tree 2 fits the new residuals. Update: F₂(x) = F₁(x) + 0.1 × h₂(x).

Continue for 150 steps. Each tree focuses on the mistakes of all previous trees combined.

Step 150: The final ensemble F₁₅₀(x) produces probability p(x) = 1 / (1 + exp(-F₁₅₀(x))). If p(x) > 0.5, classify as fraud (class 1); otherwise not fraud (class 0).

#### Hyperparameter Effects

| Parameter | Our Value | Effect if Too High | Effect if Too Low |
|-----------|-----------|-------------------|-------------------|
| learning_rate | 0.1 | Overfitting, training instability | Underfitting, needs more trees |
| n_estimators | 150 | Overfitting, longer training/prediction | Underfitting, insufficient capacity |
| max_depth | 4 | Overfitting, overly complex trees | Underfitting, misses feature interactions |
| subsample | 0.8 | Overfitting (no randomness for diversity) | Underfitting (too few samples per tree) |

### 11.2 Feature Relationships

The five features model a payment transaction:

Sender oldbalanceOrg → amount deducted → newbalanceOrig remains
Receiver oldbalanceDest → amount added → newbalanceDest increases

Fraud indicators: newbalanceOrig = 0 (account drained), amount >> oldbalanceOrg (unauthorized), newbalanceDest >> oldbalanceDest + amount (money laundering).

### 11.3 Expected Real-World Performance

| Metric | Synthetic | Real (est.) | Note |
|--------|-----------|-------------|------|
| Accuracy | 1.0 | 0.95-0.99 | Misleading for imbalanced data |
| Precision | 1.0 | 0.5-0.8 | Many false positives expected |
| Recall | 1.0 | 0.7-0.9 | Critical to catch real fraud |
| F1 | 1.0 | 0.6-0.8 | Harmonic mean of P and R |

---

## 12. API Security Best Practices

### 12.1 API Key Authentication

Add a middleware that checks API keys from headers:

```python
from fastapi.security import HTTPBearer
API_KEYS = os.get...S", "").split(",")

@app.middleware("http")
async def authenticate(request, call_next):
    if request.url.path in ["/health", "/ready"]:
        return await call_next(request)
    auth = request.headers.get("Authorization")
    if not auth or auth.replace("Bearer ", "") not in API_KEYS:
        raise HTTPException(401, detail="Invalid API key")
    return await call_next(request)
```

### 12.2 Rate Limiting

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(request, body):
    ...
```

### 12.3 Input Validation with Pydantic

```python
class PredictRequest(BaseModel):
    features: List[float] = Field(..., min_items=5, max_items=5)
    
    @validator("features")
    def validate_range(cls, v):
        if v[0] < 0:
            raise ValueError("Amount cannot be negative")
        if v[0] > 1_000_000:
            raise ValueError("Amount exceeds maximum")
        return v
```

---

## 13. Advanced Deployment

### 13.1 Blue-Green Deployment

Current (Blue) version v1.0 runs 100% traffic. Deploy Green (v2.0) alongside with 0% traffic. Run smoke tests on Green, then switch all traffic. Monitor for 15 minutes, then destroy Blue.

### 13.2 Canary Deployment

Phase 1: 95% v1.0 + 5% v2.0 (monitor 30 min). Phase 2: 50% each (monitor 30 min). Phase 3: 100% v2.0. Rollback is instant — just revert to 100% v1.0.

### 13.3 A/B Testing Framework

Route 90% of requests to the current model (v1, control) and 10% to an experimental model (v2, treatment). Log which version served each request for analysis. Compare accuracy, latency, and business metrics before promoting v2.

---

## 14. Monitoring & Alerting

### 14.1 Alert Rules Summary

| Alert Name | Condition | Severity | Action |
|-----------|-----------|----------|--------|
| HighLatency | p99 latency > 1s for 5 min | Warning | Scale out, investigate |
| LowAccuracy | Accuracy < 0.8 for 10 min | Critical | Rollback model version |
| DataDrift | drift_score > 0.3 for 15 min | Warning | Notify DS team, retrain |
| ESUnreachable | ES connection fails for 5 min | Critical | Check network/ES cluster |

### 14.2 Structured Logging

Replace print statements with structured JSON logs for ELK parsing:

```json
{
  "timestamp": "2026-06-30T14:30:25.174Z",
  "level": "INFO",
  "service": "ml-inference",
  "request_id": "a1b2c3d4-...",
  "prediction": {"label": "0", "confidence": 0.9999},
  "latency_ms": 0.711
}
```

---

## 15. Cost Analysis

### 15.1 Monthly Cost Estimates

| Setup | Components | Monthly Cost |
|-------|-----------|-------------|
| AWS ECS Fargate | 1 vCPU, 2GB RAM, ALB + 3 ES t3.medium | ~$225 |
| AWS EKS | 3 x t3.medium nodes + control plane + ALB | ~$283 |
| On-Premise (yours) | Existing ES cluster + hardware | ~$0 |

### 15.2 Optimization Strategies

Spot instances save 60-70% for batch inference but can be interrupted. ES index lifecycle management (delete after 30 days) saves storage costs. Model quantization (int8) reduces memory by 75% with minimal accuracy loss.

---

## 16. Compliance & Governance

### 16.1 Model Card

model: fraud-detector v1.0.0
training: 10K synthetic rows, 0.91% fraud rate, 5 numeric features
limitations: Synthetic data only — may not generalize to real transaction patterns
intended use: First-pass fraud screening, augmenting human review, never sole decision-maker

### 16.2 Retention Policy

Inference logs: 30 days (audit, debugging). Metrics: 90 days (trend analysis). Drift reports: 1 year (compliance). Model artifacts: indefinite (reproducibility).

---

## 17. Extending the Project

### 17.1 Multi-Model Support

Add a registry of models and a path parameter to select which model to use:

```python
@app.post("/predict/{model_name}")
async def predict(model_name: str, body: PredictRequest):
    model = MODELS.get(model_name)
    if not model:
        raise HTTPException(404, f"Model {model_name} not found")
    ...
```

### 17.2 Batch Inference

Accept a list of requests and return predictions in bulk. This improves throughput for offline/batch processing workloads.

### 17.3 Model Warm-up

Run a dummy prediction during server startup to eliminate first-request cold-start latency:

```python
dummy = np.array([[250.0, 5000.0, 4750.0, 2000.0, 2250.0]])
_ = model.predict(dummy)
_ = model.predict_proba(dummy)
```

---

## 18. Conclusion

This project is a complete, production-ready ML inference service. Key design decisions include FastAPI for async performance and auto-documentation, Elasticsearch for scalable observability, fire-and-forget telemetry to avoid blocking predictions, sidecar metrics collection for separation of concerns, and multi-stage Docker builds for minimal image size.

### Next Learning Steps

Amazon SageMaker for managed MLOps, MLflow for experiment tracking, Kubeflow for ML pipelines, Apache Kafka for event-driven inference logging, and DVC for data versioning in ML projects.

---

*© 2026 ML Inference Service. Built for MLOps learning.*
