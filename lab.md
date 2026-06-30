# ML Inference Service — Lab Exercises

![Labs](https://img.shields.io/badge/Labs-10%20Exercises-brightgreen)
![Difficulty](https://img.shields.io/badge/Difficulty-Beginner--Advanced-orange)
![Time](https://img.shields.io/badge/Time-4--6%20Hours-blue)

---

## 📑 Lab Index

| Lab | Title | Difficulty | Time | Topics |
|-----|-------|-----------|------|--------|
| 1 | Environment Setup & Project Structure | Beginner | 30 min | Python, Git, Dependencies |
| 2 | Model Training & Understanding | Beginner | 30 min | scikit-learn, Pipeline, Serialization |
| 3 | Running the Inference Server | Beginner | 30 min | FastAPI, uvicorn, Endpoints |
| 4 | Making Predictions | Beginner | 30 min | curl, REST API, JSON |
| 5 | Error Handling & Edge Cases | Intermediate | 30 min | Validation, Error Codes |
| 6 | Elasticsearch Integration | Intermediate | 45 min | ES Connection, Indexing, Search |
| 7 | Metrics Collection & Analysis | Intermediate | 45 min | Performance Metrics, Latency |
| 8 | Data Drift Detection | Advanced | 45 min | Evidently, Feature Distribution |
| 9 | Docker & Containerization | Intermediate | 45 min | Dockerfile, Build, Run |
| 10 | Production Hardening | Advanced | 45 min | Security, Config, Monitoring |

**Total Time:** ~4-6 hours
**Prerequisites:** Python 3.11+, pip, curl, text editor, ES 8.x (for Labs 6-8)

---

## How to Use This Lab

Each lab contains:

1. **Learning Objectives** — ဒီ lab ပြီးရင် ဘာတွေတတ်မြောက်သွားမလဲ
2. **Background Theory** — လိုအပ်တဲ့ သီအိုရီရှင်းလင်းချက်
3. **Step-by-Step Tasks** — လက်တွေ့ဆောင်ရွက်ရန် အဆင့်များ
4. **Verification Steps** — မှန်ကန်ကြောင်းစစ်ဆေးရန်
5. **Questions** — ကိုယ်တိုင်စဉ်းစားရန် မေးခွန်းများ
6. **Hint Box** — ခက်ခဲရင်ဖွင့်ကြည့်ရန် အရိပ်အမြွက်

Solutions ကို `solution.md` မှာကြည့်ပါ။

---

## Lab 1: Environment Setup & Project Structure

### Learning Objectives

ဒီ Lab ပြီးရင် သင်တတ်မြောက်သွားမည့်အချက်များ:

1. Python virtual environment ဆောက်တတ်ခြင်း
2. pip/uv နဲ့ dependencies သွင်းတတ်ခြင်း
3. Project structure ကိုနားလည်ခြင်း
4. File တစ်ခုချင်းစီရဲ့အလုပ်လုပ်ပုံကိုသိခြင်း

### Background Theory

#### 1.1 Python Virtual Environment ဆိုတာဘာလဲ?

Virtual environment ဆိုတာ Python project တစ်ခုချင်းစီအတွက်
**သီးသန့် package space** တစ်ခုဖြစ်တယ်။ ဒါက ဘာကြောင့်အရေးကြီးလဲဆိုတော့:

- Project A က `flask==2.0` လိုအပ်တယ်
- Project B က `flask==3.0` လိုအပ်တယ်
- Virtual environment မသုံးရင် တစ်ခုနဲ့တစ်ခု conflict ဖြစ်မယ်

#### 1.2 pip vs uv

| Tool | Speed | Features |
|------|-------|----------|
| `pip` | Slower | Python built-in, stable |
| `uv` | 10-100x faster | Rust-based, compatibility mode |

#### 1.3 requirements.txt Format

```
package==1.0.0    # Exact version (recommended)
package>=1.0.0    # Minimum version
package~=1.0.0    # Compatible release
package           # Any version (not recommended for production)
```

### Step-by-Step Tasks

#### Task 1.1: Clone/Download the Project

```bash
# If you have git:
git clone <your-repo-url> ml-inference
cd ml-inference

# If you downloaded ZIP:
# Extract to your workspace and cd into it
```

**Check:**
```bash
ls -la
# You should see: README.md  Dockerfile  app/  model/  data/
```

#### Task 1.2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

**Check:**
```bash
which python
# Should show: .../ml-inference/.venv/bin/python

pip --version
# Should show the venv path
```

#### Task 1.3: Install Dependencies

```bash
# pip (slower but reliable)
pip install -r app/requirements.txt

# OR uv (faster)
uv pip install -r app/requirements.txt
```

**Check:**
```bash
python -c "
import fastapi, uvicorn, sklearn, numpy, pandas, joblib, elasticsearch
print('All packages installed successfully!')
print(f'FastAPI: {fastapi.__version__}')
print(f'scikit-learn: {sklearn.__version__}')
print(f'numpy: {numpy.__version__}')
print(f'pandas: {pandas.__version__}')
print(f'elasticsearch: {elasticsearch.__version__}')
"
```

#### Task 1.4: Explore Project Structure

```bash
# List all files
find . -type f -not -path '*/\.*' -not -path '*__pycache__*' | sort

# Read requirements.txt
cat app/requirements.txt

# Read __init__.py
cat app/__init__.py
```

#### Task 1.5: Understand Each File's Purpose

ဖိုင်တစ်ခုချင်းစီရဲ့အကြောင်းကို README.md မှာဖတ်ပြီး
အောက်ပါဇယားကိုဖြည့်ပါ:

| File Name | Purpose (၃-၅ word) | Main Class/Function |
|-----------|--------------------|--------------------|
| `app/main.py` | | |
| `app/monitor.py` | | |
| `app/collect_metrics.py` | | |
| `app/train_model.py` | | |

#### Task 1.6: Examine Requirements in Detail

Package တစ်ခုချင်းစီရဲ့ version ကိုစစ်ဆေးပါ:

```bash
python -c "
import pkg_resources
packages = ['fastapi', 'uvicorn', 'pydantic', 'elasticsearch',
            'scikit-learn', 'numpy', 'pandas', 'joblib']
for p in packages:
    try:
        v = pkg_resources.get_distribution(p).version
        print(f'{p:30s} {v}')
    except:
        print(f'{p:30s} NOT INSTALLED')
"
```

### Verification Steps

- [ ] Virtual environment activated (သင့် terminal prompt မှာ `(.venv)` ပါလား?)
- [ ] `pip list` မှာ packages အားလုံးပါလား?
- [ ] `python -c "import fastapi"` error မရှိဘူးလား?
- [ ] Project folder structure က README နဲ့ကိုက်လား?

### Questions

1. ဘာကြောင့် `requirements.txt` မှာ version တွေကို `==` နဲ့ pin ထားတာလဲ?
2. `uvicorn[standard]` ဆိုတဲ့ `[standard]` က ဘာအတွက်လဲ?
3. Virtual environment မသုံးရင် ဘာဖြစ်နိုင်လဲ?
4. `pydantic` package က ဘာအတွက်လိုအပ်တာလဲ?

---

## Lab 2: Model Training & Understanding

### Learning Objectives

1. scikit-learn pipeline ကိုနားလည်ခြင်း
2. Synthetic data generation ကိုသိခြင်း
3. Model serialization (joblib) ကိုနားလည်ခြင်း
4. Model evaluation metrics ကိုသိခြင်း

### Background Theory

#### 2.1 GradientBoostingClassifier ဆိုတာဘာလဲ?

Gradient Boosting က **ensemble learning** method တစ်မျိုးဖြစ်တယ်။
ဆိုလိုတာက model တစ်ခုတည်းမဟုတ်ဘဲ decision tree အများကြီးကိုပေါင်းပြီး
ခန့်မှန်းတာပဲ။

**ဘယ်လိုအလုပ်လုပ်လဲ:**

```
Step 1: First tree က data ကိုကြည့်ပြီး ခန့်မှန်းတယ်
        → Error တွေရှိတယ် (မှားတဲ့ predictions)

Step 2: Second tree က first tree ရဲ့ error တွေကိုပြင်တယ်
        → Error နည်းသွားတယ်

Step 3: Third tree က second tree ရဲ့ error တွေကိုပြင်တယ်
        → Error ပိုနည်းသွားတယ်

... (150 ကြိမ်အထိ)

Final: Tree တွေအကုန်လုံးရဲ့ ခန့်မှန်းချက်ကိုပေါင်းပြီး final prediction လုပ်တယ်
```

**Note:** ဒါက microservice architecture မှာ
service တစ်ခုချင်းစီက တစ်စိတ်တစ်ပိုင်းစီတွက်ပြီး aggregate လုပ်သလိုပဲ —
tree တစ်ခုချင်းစီက error ရဲ့တစ်စိတ်တစ်ပိုင်းကိုပြင်တယ်။

#### 2.2 RobustScaler ဆိုတာဘာလဲ?

Feature scaling technique တစ်မျိုးဖြစ်တယ်။

**StandardScaler:**
```
z = (x - mean) / std
— Outlier တွေကို sensitive ဖြစ်တယ်
— Mean နဲ့ std က outlier တွေကြောင့်ပြောင်းသွားနိုင်တယ်
```

**RobustScaler (ဒီမှာသုံးထားတာ):**
```
z = (x - median) / IQR
— Outlier တွေကို resistant ဖြစ်တယ်
— Median နဲ့ IQR က outlier တွေကြောင့်မပြောင်းဘူး
— Fraud data မှာ amount တန်ဖိုးတွေက extreme ဖြစ်တတ်တယ်
```

#### 2.3 Synthetic Data Generation

ဒီ project မှာ real transaction data မရှိလို့ **synthetic data** ကိုသုံးထားတယ်။
ဒါက real world ရဲ့ pattern ကိုတုပထားတာပဲ — အတိအကျမဟုတ်ဘူး။

**Fraud Pattern:**
- ငွေပမာဏ များတယ် ($5,000 - $50,000)
- ပေးပို့သူရဲ့လက်ကျန် ၀ သွားတယ် (ငွေအကုန်ထုတ်)
- ပေးပို့သူရဲ့မူလလက်ကျန်များတယ်

### Step-by-Step Tasks

#### Task 2.1: Run Training Script

```bash
cd ml-inference
python -m app.train_model
```

**Expected Output:**
```
2026-XX-XX XX:XX:XX,XXX | Training fraud-detection model (raw vector pipeline)...
2026-XX-XX XX:XX:XX,XXX | Generated 10000 rows (fraud rate = 0.0091)
2026-XX-XX XX:XX:XX,XXX | Train accuracy: 1.0000
2026-XX-XX XX:XX:XX,XXX | Test accuracy:  1.0000
2026-XX-XX XX:XX:XX,XXX | Sample pred=0 proba=[0.9999, 0.0001]
2026-XX-XX XX:XX:XX,XXX | Model saved to .../model/model.pkl
```

#### Task 2.2: Examine the Generated Data

```python
# Run in Python
import pandas as pd
import numpy as np

df = pd.read_csv("data/sample_data.csv")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\nFraud rate: {df['isFraud'].mean():.4f}")
print(f"\nFeature statistics:")
print(df.describe())
print(f"\nFraud vs Non-Fraud comparison:")
print(df.groupby("isFraud").describe().T)
```

**Q:** Fraud နဲ့ non-fraud ကြား feature တန်ဖိုးတွေဘယ်လိုကွာလဲ?

#### Task 2.3: Load and Inspect the Trained Model

```python
import joblib
import numpy as np

pipeline = joblib.load("model/model.pkl")
print(f"Pipeline type: {type(pipeline)}")
print(f"Pipeline steps: {[s[0] for s in pipeline.steps]}")

# Get the classifier
clf = pipeline.named_steps["classifier"]
print(f"Classifier: {type(clf).__name__}")
print(f"Number of trees: {clf.n_estimators}")
print(f"Max depth: {clf.max_depth}")
print(f"Learning rate: {clf.learning_rate}")
print(f"Total parameters: {clf.n_estimators * clf.max_depth} trees")
```

#### Task 2.4: Make a Test Prediction

```python
import joblib
import numpy as np

pipeline = joblib.load("model/model.pkl")

# Normal transaction
normal = np.array([[250.0, 5000.0, 4750.0, 2000.0, 2250.0]])
pred = pipeline.predict(normal)
proba = pipeline.predict_proba(normal)
print(f"Normal transaction:")
print(f"  Prediction: {pred[0]} ({'fraud' if pred[0] else 'not fraud'})")
print(f"  Confidence: {max(proba[0]):.4f}")
print(f"  Probabilities: {proba[0]}")

# Fraud transaction
fraud = np.array([[45000.0, 200000.0, 0.0, 5000.0, 50000.0]])
pred = pipeline.predict(fraud)
proba = pipeline.predict_proba(fraud)
print(f"\nFraud transaction:")
print(f"  Prediction: {pred[0]} ({'fraud' if pred[0] else 'not fraud'})")
print(f"  Confidence: {max(proba[0]):.4f}")
print(f"  Probabilities: {proba[0]}")
```

#### Task 2.5: Experiment with Different Inputs

```python
# Try different values and see how confidence changes
test_cases = [
    ([10.0, 100.0, 90.0, 50.0, 60.0], "Very small transaction"),
    ([500.0, 10000.0, 9500.0, 5000.0, 5500.0], "Normal transaction"),
    ([5000.0, 50000.0, 45000.0, 10000.0, 15000.0], "Large but normal"),
    ([25000.0, 100000.0, 0.0, 2000.0, 27000.0], "Suspicious (balance zeroed)"),
    ([100000.0, 500000.0, 0.0, 100.0, 100100.0], "Very suspicious"),
]

for features, desc in test_cases:
    X = np.array([features])
    pred = pipeline.predict(X)[0]
    conf = max(pipeline.predict_proba(X)[0])
    print(f"{desc:30s} → {'FRAUD' if pred else 'safe'} (conf={conf:.4f}) features={features}")
```

**Q:** ဘယ် feature combination က fraud ဖြစ်နိုင်ခြေများလဲ? ဘာကြောင့်လဲ?

#### Task 2.6: Understand Pipeline Serialization

```python
import joblib
import os

# Check file size
size = os.path.getsize("model/model.pkl")
print(f"Model file size: {size:,} bytes ({size/1024:.1f} KB)")

# Load and examine internals
pipeline = joblib.load("model/model.pkl")

# Feature importance
clf = pipeline.named_steps["classifier"]
feature_names = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]

importances = clf.feature_importances_
for name, imp in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
    print(f"  {name:20s} → {imp:.4f} ({imp*100:.1f}%)")
```

**Q:** ဘယ် feature က model အတွက်အရေးကြီးဆုံးလဲ?

### Verification Steps

- [ ] `model/model.pkl` file ရှိလား? (file size ~500KB+)
- [ ] `data/sample_data.csv` မှာ row 10000 ရှိလား?
- [ ] `data/reference.csv` မှာ row 1000 ရှိလား?
- [ ] Normal transaction က "not fraud" ပြန်လား?
- [ ] Fraud transaction (balance zeroed) က "fraud" ပြန်လား?

### Questions

1. ဘာကြောင့် RobustScaler ကို StandardScaler အစားသုံးတာလဲ?
2. `random_state=42` က ဘာအတွက်လဲ?
3. `n_estimators=150` က များလား/နည်းလား? ဘာကြောင့်လဲ?
4. joblib နဲ့ pickle ကွာခြားချက်ကဘာလဲ?
5. Synthetic data ရဲ့အားသာချက်/အားနည်းချက်တွေကဘာတွေလဲ?

---

## Lab 3: Running the Inference Server

### Learning Objectives

1. FastAPI application structure ကိုနားလည်ခြင်း
2. uvicorn ASGI server ကိုသုံးတတ်ခြင်း
3. Server startup/shutdown lifecycle ကိုနားလည်ခြင်း
4. Health/Readiness probes တွေကိုစမ်းသပ်ခြင်း

### Background Theory

#### 3.1 FastAPI ဆိုတာဘာလဲ?

FastAPI က Python အတွက် **modern, fast REST API framework** ဖြစ်တယ်။
ထူးခြားချက်တွေကတော့:

- **Async support** — Request တွေကို non-blocking နဲ့ handle လုပ်တယ်
- **Auto validation** — pydantic ကို သုံးပြီး request/response validation လုပ်တယ်
- **Auto docs** — `/docs` (Swagger UI) နဲ့ `/redoc` ကို auto-generate လုပ်ပေးတယ်
- **OpenAPI compliant** — Standard API specification ကိုလိုက်နာတယ်

#### 3.2 uvicorn ဆိုတာဘာလဲ?

uvicorn က **ASGI (Asynchronous Server Gateway Interface)** server ဖြစ်တယ်။
FastAPI ကို run ပေးတယ်။ သူက:

- HTTP/1.1 နဲ့ WebSocket ကို support လုပ်တယ်
- Worker processes အများကြီးနဲ့ run လို့ရတယ် (multi-core)
- Production-ready ဖြစ်တယ်

```
uvicorn vs gunicorn:

Traditional (WSGI):
  Nginx → Gunicorn → Django/Flask (sync)
  
Modern (ASGI):
  Nginx → uvicorn → FastAPI (async)
```

#### 3.3 FastAPI Lifespan Pattern

```python
@asynccontextmanager
async def lifespan(app):
    # Startup code (model loading, DB connection)
    print("Starting up...")
    model = joblib.load("model.pkl")
    yield
    # Shutdown code (cleanup)
    print("Shutting down...")
```

Startup မှာ model load လုပ်တယ် — request ကျမှ load လုပ်ရင် latency များမယ်။
Shutdown မှာ cleanup လုပ်တယ် — ဒါက preStop hook နဲ့ဆင်တယ်။

### Step-by-Step Tasks

#### Task 3.1: Start the Server (Minimal)

```bash
cd ml-inference/app

# Simplest way (uses default MODEL_PATH)
MODEL_PATH=../model/model.pkl uvicorn main:app --host 0.0.0.0 --port 8080
```

**Server က run နေတုန်း terminal အသစ်တစ်ခုဖွင့်ပြီး အောက်ပါတို့ကိုလုပ်ပါ။**

#### Task 3.2: Test Health Endpoint

```bash
curl http://localhost:8080/health
```

**Expected:**
```json
{"status": "healthy", "model_loaded": true}
```

**Try without model:**
Server ကို stop လုပ်ပြီး `MODEL_PATH` ကို မရှိတဲ့ path တစ်ခုပေးပြီး restart လုပ်ပါ:
```bash
MODEL_PATH=/nonexistent/model.pkl uvicorn main:app --host 0.0.0.0 --port 8080
```

**Q:** Health endpoint က ဘာပြန်လဲ? ဘာကြောင့် 200 OK ပြန်နေတုန်းလဲ?

#### Task 3.3: Test Readiness Endpoint

```bash
# Server အလုပ်လုပ်နေချိန်မှာ
curl http://localhost:8080/ready
```

**Expected (model loaded):**
```json
{"status": "ready"}
```

**Expected (model not loaded):**
```json
{"detail": "Model not loaded"}
```
(status code: 503 Service Unavailable)

**Q:** Liveness (`/health`) နဲ့ Readiness (`/ready`) ကွာခြားချက်ကဘာလဲ?
orchestration မှာ → Load balancer / orchestrator မှာ

#### Task 3.4: Understand Startup Logs

Server စတဲ့အခါ log output ကိုအသေးစိတ်လေ့လာပါ:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
[OK] Model loaded: ../model/model.pkl
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

**Q:** 
1. "Waiting for application startup" နဲ့ "Application startup complete" ကြားမှာ ဘာဖြစ်သွားလဲ?
2. ဒီအချိန်အတွင်းမှာ request တွေကိုလက်ခံနိုင်လား?

#### Task 3.5: Access Auto-generated Docs

```bash
# Swagger UI
curl http://localhost:8080/docs

# ReDoc
curl http://localhost:8080/redoc

# OpenAPI JSON
curl http://localhost:8080/openapi.json
```

Browser ကနေလည်းဖွင့်ကြည့်နိုင်တယ်:
- http://localhost:8080/docs
- http://localhost:8080/redoc

**Q:** Swagger UI မှာ endpoint တွေကိုတိုက်ရိုက်စမ်းသပ်လို့ရလား?

#### Task 3.6: Test with Multiple Workers

```bash
# Server ကို stop လုပ်ပြီး workers 2 နဲ့ restart လုပ်ပါ
MODEL_PATH=../model/model.pkl uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
```

**Q:** Workers 2 ဆိုတာဘာလဲ? Single worker နဲ့ဘာကွာလဲ?
Worker တစ်ခုချင်းစီမှာ model ကို သီးသန့် load လုပ်လား?

#### Task 3.7: Graceful Shutdown

Server ကို `Ctrl+C` နဲ့ stop လုပ်တဲ့အခါ အောက်ပါ log ကိုမြင်ရမယ်:

```
INFO:     Shutting down
[OK] Shutting down server context.
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
```

**Q:** ဒါက orchestration မှာ container ကိုသတ်တဲ့အခါ ဘယ်လိုအသုံးဝင်လဲ?
(TerminationGracePeriodSeconds နဲ့ဆက်စပ်ပုံ)

### Verification Steps

- [ ] Server က port 8080 မှာ run နေလား? (`curl localhost:8080/health`)
- [ ] Health endpoint က "healthy" ပြန်လား?
- [ ] Model ရှိရင် Ready endpoint က 200 OK ပြန်လား?
- [ ] Swagger UI က browser မှာပေါ်လား?
- [ ] Server log မှာ "Model loaded" message ပါလား?
- [ ] Server stop လုပ်တဲ့အခါ "Shutting down" message ပါလား?

### Questions

1. FastAPI က Flask ထက် ဘာတွေပိုကောင်းလဲ?
2. ASGI နဲ့ WSGI ကွာခြားချက်ကဘာလဲ?
3. `--reload` flag က ဘာအတွက်လဲ? Production မှာသုံးသင့်လား?
4. ဘာကြောင့် model ကို startup မှာ load လုပ်ပြီး request ကျမှ မလုပ်တာလဲ?

---

## Lab 4: Making Predictions

### Learning Objectives

1. REST API ကို curl နဲ့ခေါ်တတ်ခြင်း
2. Request/Response format ကိုနားလည်ခြင်း
3. Different input scenarios ကိုစမ်းသပ်ခြင်း
4. Response fields ရဲ့အဓိပ္ပါယ်ကိုသိခြင်း

### Background Theory

#### 4.1 REST API Fundamentals

REST API က HTTP methods ကိုသုံးပြီး resource တွေကို manipulate လုပ်တယ်:

| Method | Purpose | Our Usage |
|--------|---------|-----------|
| `GET` | Read data | `/health`, `/ready` |
| `POST` | Create data | `/predict` (create prediction) |
| `PUT` | Update data | — |
| `DELETE` | Delete data | — |

#### 4.2 HTTP Status Codes

| Code | Meaning | Our Usage |
|------|---------|-----------|
| 200 | OK | Success |
| 422 | Unprocessable Entity | Invalid request body |
| 503 | Service Unavailable | Model not loaded |

#### 4.3 JSON Format

JSON (JavaScript Object Notation) က data interchange format ဖြစ်တယ်။
Python dictionary နဲ့ဆင်တယ်:

```json
{
  "string_key": "string_value",
  "number_key": 123.45,
  "array_key": [1, 2, 3],
  "nested": {
    "inner_key": "value"
  }
}
```

### Step-by-Step Tasks

#### Task 4.1: Simple Prediction Request

Server ကို Lab 3 အတိုင်း start လုပ်ပြီး အောက်ပါတို့ကိုလုပ်ပါ။

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
```

**Expected Response:**
```json
{
  "request_id": "some-uuid",
  "label": "0",
  "label_index": 0,
  "confidence": 1.0,
  "probabilities": [1.0, 0.0],
  "latency_ms": 0.711
}
```

**Response Field Analysis:**

| Field | Value | ရှင်းလင်းချက် |
|-------|-------|----------------|
| `request_id` | UUID | ဒီ request အတွက် unique ID (tracing) |
| `label` | "0" | Human-readable class (0 = not fraud, 1 = fraud) |
| `label_index` | 0 | Numeric class (model output) |
| `confidence` | 0.9999 | Model ရဲ့သေချာမှု (0-1) |
| `probabilities` | [0.9999, 0.0001] | Class တစ်ခုချင်းစီအတွက် probability |
| `latency_ms` | 0.711 | Total time in milliseconds |

#### Task 4.2: Test Fraud Detection

```bash
# High amount, sender balance zeroed → fraud
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [99999.0, 500000.0, 0.0, 100.0, 100100.0]}' | python -m json.tool
```

**Q:** Response မှာ ဘာတွေပြောင်းသွားလဲ?
- label က ဘာဖြစ်သွားလဲ?
- confidence က ဘယ်လောက်လဲ?
- Probabilities က ဘယ်လိုပြောင်းသွားလဲ?

#### Task 4.3: Test with Custom Labels

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0],
    "labels": ["not_fraud", "fraud"]
  }' | python -m json.tool
```

**Q:** `label` field က ဘာဖြစ်သွားလဲ? Labels မပါရင်ရော?

#### Task 4.4: Test Multiple Scenarios

အောက်ပါ test cases တွေကိုစမ်းသပ်ပြီး result ကိုမှတ်တမ်းတင်ပါ:

```bash
# Case 1: Normal small transaction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [10.0, 100.0, 90.0, 50.0, 60.0]}'

# Case 2: Large but normal transaction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5000.0, 50000.0, 45000.0, 10000.0, 15000.0]}'

# Case 3: Suspicious (balance almost zeroed)
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [20000.0, 100000.0, 500.0, 2000.0, 22000.0]}'

# Case 4: Classic fraud pattern
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [50000.0, 300000.0, 0.0, 1000.0, 51000.0]}'
```

**Results Table ဖြည့်ပါ:**

| Case | Description | Label | Confidence | Latency (ms) |
|------|------------|-------|------------|--------------|
| 1 | Small transaction | | | |
| 2 | Large but normal | | | |
| 3 | Balance almost zeroed | | | |
| 4 | Classic fraud | | | |

#### Task 4.5: Test with Missing/Invalid Data

```bash
# Empty features array
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": []}'

# Too many features
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1, 2, 3, 4, 5, 6, 7, 8]}'

# Missing features field
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{}'

# Wrong data type
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": ["a", "b", "c", "d", "e"]}'
```

**Q:** ဘယ် error code တွေပြန်လဲ? Error message က ဘာပြောလဲ?

#### Task 4.6: Measure Latency with `time` Command

```bash
# Using bash built-in time
time curl -s -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' > /dev/null
```

**Q:** `time` ရဲ့ real/user/sys time တွေက ဘာကိုပြတာလဲ?
Response ထဲက `latency_ms` နဲ့ `real` time ကွာခြားချက်ကဘာလဲ?

#### Task 4.7: Send Multiple Requests in Parallel

```bash
# Send 10 requests in parallel
for i in $(seq 1 10); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' &
done
wait
echo "All 10 requests completed"
```

**Q:** Latency တွေဘယ်လိုရှိလဲ? Single request နဲ့ယှဉ်ရင် ပိုများလား?
Parallel requests တွေကို server က ဘယ်လို handle လုပ်လဲ?

### Verification Steps

- [ ] Normal transaction → label "0" (not fraud)
- [ ] Fraud transaction → label "1" (fraud)
- [ ] Custom labels → label က သတ်မှတ်ထားတဲ့အတိုင်းပြန်လား?
- [ ] Invalid data → 422 Unprocessable Entity
- [ ] All responses မှာ `request_id` ပါလား?
- [ ] Latency က 1-5ms အတွင်းလား?

### Questions

1. ဘာကြောင့် features တွေကို dict မဟုတ်ဘဲ list of float အနေနဲ့ပို့တာလဲ?
2. Request တစ်ခုမှာ `ground_truth` field က ဘာအတွက်ရည်ရွယ်ထားလဲ?
3. HTTP 503 error က ဘယ်အချိန်မှာပြန်လဲ?
4. Response ထဲမှာ `probabilities` က ဘာကြောင့်အရေးကြီးလဲ? (label တစ်ခုတည်းမဟုတ်ဘဲ)

---

## Lab 5: Error Handling & Edge Cases

### Learning Objectives

1. HTTP error codes ကိုနားလည်ခြင်း
2. Input validation ကိုစမ်းသပ်ခြင်း
3. Server error scenarios ကိုလေ့လာခြင်း
4. Graceful degradation ကိုနားလည်ခြင်း

### Background Theory

#### 5.1 HTTP Error Codes

| Code | Name | Meaning | Our usage |
|------|------|---------|-----------|
| 400 | Bad Request | Client error (malformed syntax) | (automatic by FastAPI) |
| 422 | Unprocessable Entity | Validation error | Wrong data types, missing fields |
| 500 | Internal Server Error | Server crashed | Unexpected exceptions |
| 503 | Service Unavailable | Server can't handle request | Model not loaded |

#### 5.2 FastAPI Validation ဘယ်လိုအလုပ်လုပ်လဲ?

FastAPI က pydantic ကိုသုံးပြီး request body ကို auto-validate လုပ်တယ်:

```python
class PredictRequest(BaseModel):
    features: List[float]    # Must be list of floats
    labels: Optional[List[str]] = None  # Optional list of strings
    ground_truth: Optional[int] = None  # Optional integer
```

Validation မအောင်ရင် FastAPI က **422 Unprocessable Entity** ကို
error details နဲ့အတူ auto-return လုပ်တယ်။

### Step-by-Step Tasks

#### Task 5.1: Test Invalid Data Types

```bash
# String instead of number
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": ["abc", 5000.0, 4750.0, 2000.0, 2250.0]}' | python -m json.tool
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "type": "float_parsing",
      "loc": ["body", "features", 0],
      "msg": "Input should be a valid number, unable to parse string as a number",
      "input": "abc"
    }
  ]
}
```

**Q:** `loc` field က ဘာကိုဆိုလိုတာလဲ? Error ရဲ့တည်နေရာကိုဘယ်လိုဖော်ပြလဲ?

#### Task 5.2: Test Missing Field

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{}' | python -m json.tool
```

**Q:** Error message က ဘာပြောလဲ? ဘယ် field က missing ဖြစ်နေလဲ?

#### Task 5.3: Test Wrong Feature Count

```bash
# Too few features
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0]}'

# Too many features
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]}'
```

**Q:** ဒီ error က 422 လား 500 လား? ဘာကြောင့်လဲ?
Feature count ကိုက်ညီမှုကို pydantic က check လုပ်လား? Model က check လုပ်လား?

#### Task 5.4: Test Server-Start-without-Model

```bash
# Server ကို model မရှိဘဲ start လုပ်ပါ
cd ml-inference/app
MODEL_PATH=/nonexistent.pkl uvicorn main:app --host 0.0.0.0 --port 8081

# အခြား terminal မှာ
curl http://localhost:8081/health
curl http://localhost:8081/ready
curl -X POST http://localhost:8081/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
```

**Q:** 
- Health endpoint က ဘာပြန်လဲ? ဘာကြောင့် 200 OK ပြန်နေတုန်းလဲ?
- Ready endpoint က ဘာပြန်လဲ?
- Predict endpoint က ဘာပြန်လဲ? Status code ကဘာလဲ?

**ဒါက Graceful Degradation ရဲ့ဥပမာပဲ:**
- Server က model မရှိပေမယ့် ဆက်အလုပ်လုပ်တယ် (health check pass)
- Ready check က fail ဖြစ်တယ် (orchestration က traffic မပို့ဘူး)
- Predict ကို 503 ပြန်တယ် (client က retry လုပ်လို့ရတယ်)

#### Task 5.5: Test Concurrent Requests with One Worker

```bash
# Single worker နဲ့ run ပါ
MODEL_PATH=../model/model.pkl uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1

# 20 requests တစ်ပြိုင်နက်ပို့ပါ
for i in $(seq 1 20); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' &
done
wait
echo "All done"
```

**Q:** Request တွေက queue လုပ်လား? တစ်ပြိုင်နက်တည်း run လား?
Worker 1 ပဲရှိရင် parallel requests ကိုဘယ်လို handle လုပ်လဲ?

#### Task 5.6: Test Request Timeout

```bash
# Timeout 1ms ထားပြီး request ပို့ကြည့်
curl --max-time 0.001 -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
```

**Q:** `curl: (28) Connection timed out` error ရလား?
Production မှာ timeout ကိုဘယ်လိုကာကွယ်သင့်လဲ?

### Verification Steps

- [ ] String features → 422 error
- [ ] Empty body → 422 error (features missing)
- [ ] Model not loaded → predict returns 503
- [ ] Model not loaded → ready returns 503
- [ ] Model not loaded → health returns 200
- [ ] Error responses မှာ `detail` field ပါလား?
- [ ] Error messages က ဖတ်လို့ကောင်းလား? (user-friendly?)

### Questions

1. FastAPI က error handling ကို Flask နဲ့ယှဉ်ရင် ဘယ်လိုကွာလဲ?
2. 422 နဲ့ 400 error code ကွာခြားချက်ကဘာလဲ?
3. ဘာကြောင့် `except Exception` ကိုသုံးပြီး predict error ကို generic ဖမ်းထားတာလဲ?
4. Production မှာ error handling ကိုဘယ်လို improve လုပ်သင့်လဲ?
(Structured logging, error tracking, alerting)

---

## Lab 6: Elasticsearch Integration

### Learning Objectives

1. ES client configuration ကိုနားလည်ခြင်း
2. ES index structure ကိုသိခြင်း
3. Inference logs တွေကို ES မှာကြည့်တတ်ခြင်း
4. ES query ရေးတတ်ခြင်း

### Background Theory

#### 6.1 Elasticsearch ဆိုတာဘာလဲ?

Elasticsearch က **distributed search and analytics engine** ဖြစ်တယ်။
ဒီ project မှာ:

1. **Inference log storage** — request တစ်ခုချင်းစီရဲ့ details
2. **Metrics storage** — Aggregated performance metrics
3. **Drift detection storage** — Data drift reports
4. **Search** — Recent logs ကိုရှာဖို့

#### 6.2 ES Index vs RDBMS Table

| ES Concept | RDBMS Equivalent |
|------------|-----------------|
| Index | Table |
| Document | Row |
| Field | Column |
| Mapping | Schema |
| Query DSL | SQL |
| Shard | Partition |

#### 6.3 ES Client Version Compatibility

ဒီ project မှာ elasticsearch-py **8.12.0** ကိုသုံးထားတယ်။
**ဘာကြောင့် 8.12.0 လဲ?**

- `9.x` client → ES 8.19.17 server → ❌ (Accept header mismatch)
- `8.13.0` → Windows opentelemetry issue → ❌
- `8.12.0` → ES 8.19.17 server → ✅

#### 6.4 InferenceMonitor Class Flow

```
InferenceMonitor.__init__()
  ├─ Read ES_HOST, ES_USER, ES_PASS from env
  ├─ Create Elasticsearch client
  ├─ Set index names: ml-inference, ml-metrics
  └─ Set deployment metadata (model_name, pod_name, etc.)

InferenceMonitor.log_inference()
  ├─ Build document dict
  ├─ es.index(index="ml-inference", document=doc)
  └─ On error: print warning (never crash)

InferenceMonitor.log_performance_metrics()
  ├─ Compute sklearn metrics
  ├─ Compute latency percentiles
  ├─ es.index(index="ml-metrics", document=doc)
  └─ On error: print warning

InferenceMonitor.log_drift()
  ├─ Run Evidently DataDriftPreset
  ├─ Extract drifted features
  ├─ es.index(index="ml-metrics", document=doc)
  └─ On error: print warning
```

### Step-by-Step Tasks

#### Task 6.1: Verify ES Connection (Without Server)

```python
# test_es_connection.py
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    "http://192.168.1.123:80",
    basic_auth=("elastic", "ML0psElk!2026")
)

# Test 1: Connection
info = es.info()
print(f"ES Version: {info['version']['number']}")
print(f"Cluster: {info['cluster_name']}")
print(f"Cluster UUID: {info['cluster_uuid']}")

# Test 2: List indices
indices = es.cat.indices(format="json")
print(f"\nTotal indices: {len(indices)}")
for idx in indices[:10]:  # First 10
    print(f"  {idx['index']:30s} {idx['health']:5s} docs={idx['docs.count']}")
```

#### Task 6.2: Write a Test Document

```python
from elasticsearch import Elasticsearch
from datetime import datetime, timezone

es = Elasticsearch(
    "http://192.168.1.123:80",
    basic_auth=("elastic", "ML0psElk!2026")
)

doc = {
    "@timestamp": datetime.now(timezone.utc).isoformat(),
    "request_id": "test-manual-write",
    "model_name": "fraud-detector",
    "test_purpose": "manual test from lab",
    "features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0],
    "prediction": {
        "label": "0",
        "label_index": 0,
        "confidence": 0.9999,
        "probabilities": [0.9999, 0.0001]
    },
    "performance": {
        "latency_ms": 1.234,
    },
    "status": "success"
}

resp = es.index(index="ml-inference", document=doc)
print(f"Index result: {resp['result']}")
print(f"Document ID: {resp['_id']}")
```

#### Task 6.3: Search Your Test Document

```bash
# Using curl
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?q=request_id:test-manual-write&pretty"
```

```python
# Using Python
resp = es.search(
    index="ml-inference",
    query={"term": {"request_id": "test-manual-write"}}
)
print(f"Total matches: {resp['hits']['total']['value']}")
for hit in resp['hits']['hits']:
    print(f"  Score: {hit['_score']}")
    print(f"  Source: {hit['_source']}")
```

**Q:** _score ဆိုတာဘာလဲ? Term query နဲ့ match query ကွာခြားချက်ကဘာလဲ?

#### Task 6.4: Start Server with ES and Make Predictions

```bash
cd ml-inference/app

MODEL_PATH=../model/model.pkl \
ES_HOST=http://192.168.1.123:80 \
ES_USER=elastic \
ES_PASS='ML0psElk!2026' \
uvicorn main:app --host 0.0.0.0 --port 8080
```

Predictions ၃-၄ ခုလုပ်ပါ:
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'

curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [99999.0, 500000.0, 0.0, 100.0, 100100.0]}'

curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [500.0, 10000.0, 9500.0, 5000.0, 5500.0]}'
```

#### Task 6.5: Search and Analyze ES Documents

```bash
# Latest 3 documents
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?size=3&sort=@timestamp:desc&pretty"

# Count by status
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_count?pretty"

# Count by prediction label
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "size": 0,
    "aggs": {
      "by_label": {
        "terms": {"field": "prediction.label_index"}
      }
    }
  }'
```

**Q:** Aggregation query က ဘာပြန်လဲ? Prediction 0 နဲ့ 1 ဘယ်နှစ်ခုစီရှိလဲ?

#### Task 6.6: Check ES Client Version

```python
import elasticsearch
print(f"ES client version: {elasticsearch.__version__}")

import elastic_transport
print(f"ES transport version: {elastic_transport.__version__}")
```

**Q:** သင့် client version က server version (8.19.17) နဲ့ကိုက်လား?
မကိုက်ရင် ဘာဖြစ်နိုင်လဲ?

#### Task 6.7: Test Monitor Error Handling (ES Down)

```bash
# ES_HOST ကို မရှိတဲ့ host တစ်ခုပေးပြီး server ကို restart လုပ်ပါ
MODEL_PATH=../model/model.pkl \
ES_HOST=http://192.168.1.999:80 \
uvicorn main:app --host 0.0.0.0 --port 8080
```

Prediction လုပ်ကြည့်ပါ:
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
```

**Q:**
- Prediction က success ဖြစ်လား?
- Server log မှာ `[WARN]` message ပါလား?
- Response time က ပုံမှန်အတိုင်းလား?

**ဒါက Fire-and-Forget Pattern ရဲ့အားသာချက်ပဲ — ES က down ဖြစ်နေရင်တောင်
inference service က ဆက်အလုပ်လုပ်တယ်။**

### Verification Steps

- [ ] ES connection test success (info() က version ပြန်လား?)
- [ ] Manual document write success (result = "created")
- [ ] Search query က document ကိုပြန်ရှာတွေ့လား?
- [ ] Server က predict လုပ်တိုင်း ES index ထဲ doc တက်လား?
- [ ] ES down ရင် server က မပျက်ဘူးလား? (graceful degradation)
- [ ] Aggregation query အလုပ်လုပ်လား?

### Questions

1. ES 8.x client က ES 9.x server နဲ့အလုပ်လုပ်လား? ဘာကြောင့်လဲ?
2. Fire-and-forget pattern ရဲ့အားသာချက်နဲ့အားနည်းချက်တွေကဘာတွေလဲ?
3. Production မှာ ES ကို ပိုပြီး reliable ဖြစ်အောင်ဘယ်လိုလုပ်မလဲ?
(Retry, circuit breaker, buffer queue, dead letter queue)
4. ES index mapping ကို ဘာကြောင့် pre-define လုပ်သင့်တာလဲ?
(Mapping explosion, field type conflicts)

---

## Lab 7: Metrics Collection & Analysis

### Learning Objectives

1. collect_metrics.py ရဲ့အလုပ်လုပ်ပုံကိုနားလည်ခြင်း
2. Performance metrics (accuracy, precision, recall, F1) တွက်တတ်ခြင်း
3. Latency percentiles (p95, p99) ကိုနားလည်ခြင်း
4. ES queries နဲ့ metrics ကိုခွဲခြမ်းစိတ်ဖြာခြင်း

### Background Theory

#### 7.1 Classification Metrics

**Confusion Matrix:**

```
                  Actual
              Fraud    Not Fraud
Predicted  ┌────────┬──────────┐
  Fraud    │   TP   │    FP    │
           ├────────┼──────────┤
  Not Fraud│   FN   │    TN    │
           └────────┴──────────┘
```

TP = True Positive (fraud ကို fraud လို့ပြောတယ်)
FP = False Positive (not fraud ကို fraud လို့ပြောတယ်)
FN = False Negative (fraud ကို not fraud လို့ပြောတယ်)
TN = True Negative (not fraud ကို not fraud လို့ပြောတယ်)

**Accuracy = (TP + TN) / (TP + TN + FP + FN)**
- အားသာချက်: ရှင်းတယ်, နားလည်လွယ်တယ်
- အားနည်းချက်: Imbalanced data အတွက်မကောင်းဘူး
- ဥပမာ: Fraud 1% ပဲရှိတဲ့ data မှာ "not fraud" လို့အမြဲပြောရင် accuracy 99% ရမယ်

**Precision = TP / (TP + FP)**
- "fraud" လို့ပြောတဲ့အထဲက မှန်တဲ့အချိုး
- အားသာချက်: False positive ကိုလျှော့ချင်ရင်သုံးတယ်
- ဥပမာ: Fraud alert ကိုစစ်ဆေးတဲ့အခါ — FP များရင် အလုပ်ပိုတယ်

**Recall = TP / (TP + FN)**
- Fraud အကုန်လုံးထဲက ရှာတွေ့တဲ့အချိုး
- အားသာချက်: False negative ကိုလျှော့ချင်ရင်သုံးတယ်
- ဥပမာ: ကင်ဆာရောဂါရှာဖွေတဲ့အခါ — FN ဆိုရင်အသက်ဆုံးရှုံးနိုင်တယ်

**F1 Score = 2 × (P × R) / (P + R)**
- Precision နဲ့ Recall ရဲ့ harmonic mean
- Class imbalance ရှိတဲ့အခါ accuracy ထက်ပိုကောင်းတယ်

#### 7.2 Latency Percentiles

```
Request 100 ခုကို latency အလိုက်စီပါ:

  1.   0.5ms
  2.   0.6ms
  3.   0.6ms
  ...
  50.  0.8ms    ← median (p50)
  ...
  95.  1.2ms    ← p95 (95% က ဒီထက်မြန်တယ်)
  ...
  99.  2.5ms    ← p99 (99% က ဒီထက်မြန်တယ်)
  100. 500.0ms  ← max (outlier — network spike)
```

**p95/p99 ကဘာလို့အရေးကြီးလဲ?**

Average latency က 1ms ရှိပေမယ့်:
- p95 က 10ms → 5% user တွေ နှေးတာကိုခံစားရမယ်
- p99 က 100ms → 1% user တွေ သိသိသာသာနှေးမယ်

**Google SRE ရဲ့ စည်းကမ်း:**
"Most services consider a request slow if it takes more than **p99 latency** to complete."

### Step-by-Step Tasks

#### Task 7.1: Run collect_metrics (One-shot Mode)

Server ကို Lab 6 အတိုင်း ES နဲ့ run ပြီး predictions အချို့လုပ်ထားပါ။
ပြီးရင်:

```bash
cd ml-inference/app

# One-shot run
python -m app.collect_metrics
```

**Expected Output:**
```
2026-XX-XX XX:XX:XX | Starting metrics collection cycle ...
2026-XX-XX XX:XX:XX | Fetched N inference records from ES index 'ml-inference'
2026-XX-XX XX:XX:XX | [OK] Metrics logged — acc=1.0, f1=1.0, p95=1.5ms
2026-XX-XX XX:XX:XX | Metrics cycle complete.
```

**Q:** "N" က ဘယ်လောက်လဲ? သင့် prediction အရေအတွက်နဲ့ကိုက်လား?

#### Task 7.2: Check ml-metrics Index

```bash
# Verify metrics were written
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-metrics/_search?size=1&sort=@timestamp:desc&pretty"
```

**Expected:**
```json
{
  "hits": {
    "total": {"value": 1},
    "hits": [{
      "_source": {
        "performance": {
          "accuracy": 1.0,
          "precision": 1.0,
          "recall": 1.0,
          "f1_score": 1.0,
          "total_predictions": 3,
          "avg_latency_ms": 1.234,
          "p95_latency_ms": 2.456,
          "p99_latency_ms": 3.789
        }
      }
    }]
  }
}
```

**Q:** သင့် metrics တွေက accuracy 1.0 ရှိလား? ဘာကြောင့်လဲ?
(တစ်ချက်ပြန်စဉ်းစားကြည့်ပါ — collect_metrics.py က y_true နဲ့ y_pred ကို
ဘယ်လိုယူလဲ?)

#### Task 7.3: Analyze Metrics Over Time

Multiple metrics collections လုပ်ပြီး trends ကိုလေ့လာပါ:

```bash
# Run predictions
for i in $(seq 1 5); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' > /dev/null
done

# Run metrics
python -m app.collect_metrics

# Check both metrics docs
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-metrics/_search?size=10&sort=@timestamp:desc&pretty" \
  | python -c "
import sys, json
r = json.load(sys.stdin)
for hit in r['hits']['hits']:
    p = hit['_source']['performance']
    print(f\"{hit['_source']['@timestamp'][:19]}  total={p['total_predictions']}  acc={p['accuracy']}  p95={p['p95_latency_ms']}ms\")
"
```

**Q:** Metrics တွေက time series အနေနဲ့ဘယ်လိုပြောင်းလဲလဲ?
Window တစ်ခုနဲ့တစ်ခု metrics တူညီလား? ကွဲပြားလား?

#### Task 7.4: Manual Metrics Computation

```python
# Compute metrics manually for verification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Simulated data
y_true = [0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
y_pred = [0, 0, 1, 0, 0, 1, 0, 0, 0, 0]

print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
print(f"Recall:    {recall_score(y_true, y_pred, zero_division=0):.4f}")
print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")

# Add one error
y_pred_wrong = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
print(f"\nWith one error:")
print(f"Accuracy:  {accuracy_score(y_true, y_pred_wrong):.4f}")
print(f"F1 Score:  {f1_score(y_true, y_pred_wrong):.4f}")
```

**Q:** Y_true ကို ဘယ်ကနေရမလဲ? Production မှာ ground truth collection က
ဘယ်လိုအလုပ်လုပ်သင့်လဲ?

#### Task 7.5: Latency Percentile Analysis

```python
import numpy as np

# Simulate 1000 request latencies (in ms)
np.random.seed(42)
latencies = np.random.exponential(scale=1.0, size=1000)  # Most are fast
latencies = np.append(latencies, [50, 100, 200])  # Add outliers

print(f"Count:     {len(latencies)}")
print(f"Mean:      {np.mean(latencies):.3f} ms")
print(f"Median:    {np.median(latencies):.3f} ms")
print(f"P90:       {np.percentile(latencies, 90):.3f} ms")
print(f"P95:       {np.percentile(latencies, 95):.3f} ms")
print(f"P99:       {np.percentile(latencies, 99):.3f} ms")
print(f"Max:       {np.max(latencies):.3f} ms")

# What percentage of requests are "slow" (over 5ms)?
slow_pct = np.mean(latencies > 5) * 100
print(f"\n% of requests over 5ms: {slow_pct:.1f}%")
```

**Q:** Mean က 1.5ms လောက်ရှိပေမယ့် p99 က ဘာလို့အများကြီးများနေတာလဲ?
3 outliers (50, 100, 200ms) တွေကို mean က ဘယ်လိုသက်ရောက်လဲ? p99 ကရော?

#### Task 7.6: Compare Metrics Windows

```bash
# Collect metrics at different times with different data volumes
# Run with --interval 30 (collect every 30 seconds)
python -m app.collect_metrics --interval 30
```

**Q:** Metrics ကို 30 seconds တစ်ခါစုရင် 15 minutes တစ်ခါနဲ့ဘာကွာလဲ?
မကြာခဏစုတာရဲ့အားသာချက်/အားနည်းချက်ကဘာလဲ?

### Verification Steps

- [ ] `collect_metrics` run လို့ရလား? (--interval နဲ့ရော)
- [ ] `ml-metrics` index မှာ doc တွေရှိလား?
- [ ] Metrics doc မှာ accuracy, precision, recall, f1 ပါလား?
- [ ] Metrics doc မှာ avg/p95/p99 latency ပါလား?
- [ ] ES aggregation query အလုပ်လုပ်လား?
- [ ] 5 ခုအောက် predictions ရှိရင် [SKIP] message ပြလား?

### Questions

1. ဘာကြောင့် metrics collection ကို main server မှာတန်းမလုပ်ဘဲ
   သီးသန့် process အနေနဲ့ခွဲထားတာလဲ? (Separation of concerns)
2. `average="weighted"` ဆိုတာဘာလဲ? "micro" နဲ့ "macro" နဲ့ဘာကွာလဲ?
3. `zero_division=0` က ဘာအတွက်လဲ?
4. Production မှာ real ground truth ကိုဘယ်ကနေရရှိနိုင်လဲ?
   (Manual review, user feedback, delayed labels)

---

## Lab 8: Data Drift Detection

### Learning Objectives

1. Data drift ဆိုတာဘာလဲဆိုတာနားလည်ခြင်း
2. Evidently library ကိုသုံးတတ်ခြင်း
3. Drift detection results ကိုခွဲခြမ်းစိတ်ဖြာခြင်း
4. Drift အခြေအနေမှာဘာလုပ်သင့်လဲဆိုတာသိခြင်း

### Background Theory

#### 8.1 Data Drift ဆိုတာဘာလဲ?

Data drift ဆိုတာ production data ရဲ့ distribution က
training (reference) data နဲ့ ပြောင်းသွားတဲ့အခြေအနေပဲ။

**Drift အမျိုးအစားများ:**

| Type | ရှင်းလင်းချက် | ဥပမာ |
|------|----------------|-------|
| **Covariate Drift** | Feature distribution ပြောင်းတယ် | Transaction amount တွေက $100 → $1000 ဖြစ်သွားတယ် |
| **Prior Drift** | Label distribution ပြောင်းတယ် | Fraud rate 1% → 5% ဖြစ်သွားတယ် |
| **Concept Drift** | Feature-label relationship ပြောင်းတယ် | Fraud က pattern အသစ်တွေပေါ်လာတယ် |

#### 8.2 Drift Detection ဘယ်လိုအလုပ်လုပ်လဲ?

Evidently library က feature တစ်ခုချင်းစီအတွက်
**statistical test** တွေလုပ်တယ်:

**Numerical features (ဥပမာ: amount, balance):**
- **Kolmogorov-Smirnov (KS) Test**
  - Distribution နှစ်ခုက တူညီလားဆိုတာစစ်တယ်
  - p-value < 0.05 → drift detected
  - KS statistic = 0 → distribution တူတယ်
  - KS statistic = 1 → distribution လုံးဝမတူဘူး

**Categorical features (ဥပမာ: transaction type):**
- **Chi-squared Test**
  - Category frequencies တူလားဆိုတာစစ်တယ်

#### 8.3 Drift Score တွက်နည်း

```
share_of_drifted_columns = num_drifted_features / total_features

ဥပမာ:
- Total features: 5 (amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest)
- Drifted features: 2 (amount, newbalanceOrig)
- Data drift score: 2/5 = 0.4
- dataset_drift: True (because 0.4 > 0.3 threshold)
```

### Step-by-Step Tasks

#### Task 8.1: Basic Drift Detection with Known Shift

```python
import numpy as np
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Reference data (training distribution)
np.random.seed(42)
ref = pd.DataFrame({
    "amount": np.random.normal(500, 200, 1000),
    "balance": np.random.normal(10000, 5000, 1000),
})

# Current data (no drift — same distribution)
curr_no_drift = pd.DataFrame({
    "amount": np.random.normal(500, 200, 1000),
    "balance": np.random.normal(10000, 5000, 1000),
})

# Current data (with drift — different distribution)
curr_drift = pd.DataFrame({
    "amount": np.random.normal(5000, 2000, 1000),  # Shifted!
    "balance": np.random.normal(50000, 20000, 1000),  # Shifted!
})

# Test 1: No drift
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=curr_no_drift)
result = report.as_dict()
dr = result["metrics"][0]["result"]
print(f"Test 1 — No Drift:")
print(f"  Dataset drift: {dr['dataset_drift']}")
print(f"  Drift score: {dr['share_of_drifted_columns']:.4f}")

# Test 2: With drift
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=curr_drift)
result = report.as_dict()
dr = result["metrics"][0]["result"]
print(f"Test 2 — With Drift:")
print(f"  Dataset drift: {dr['dataset_drift']}")
print(f"  Drift score: {dr['share_of_drifted_columns']:.4f}")
for col, val in dr.get("drift_by_columns", {}).items():
    print(f"  {col}: drift_detected={val.get('drift_detected')}, "
          f"statistic={val.get('statistic', 0):.4f}, "
          f"p_value={val.get('p_value', 0):.6f}")
```

**Q:** Test 1 နဲ့ Test 2 ရဲ့ရလဒ်တွေဘယ်လိုကွာလဲ?
p_value < 0.05 ဆိုတာဘာကိုဆိုလိုလဲ?

#### Task 8.2: Run collect_metrics with Drift

Server ကို ES နဲ့ run ပြီး predictions အများကြီးလုပ်ပါ (၂၀ ခုလောက်)။
ပြီးရင် collect_metrics ကို run ပါ:

```bash
cd ml-inference/app

# Make 20+ predictions
for i in $(seq 1 25); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d "{\"features\": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}" > /dev/null
done

# Run metrics (includes drift detection)
python -m app.collect_metrics
```

#### Task 8.3: Analyze Drift Results

```bash
# Check drift results in ES
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-metrics/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "exists": {"field": "drift"}
    },
    "size": 5,
    "sort": [{"@timestamp": "desc"}]
  }'
```

**Drift Document Structure:**
```json
{
  "@timestamp": "2026-06-30T...",
  "model_name": "fraud-detector",
  "drift": {
    "data_drift_score": 0.0,
    "drift_detected": false,
    "drifted_features": []
  }
}
```

**Q:** သင့် result မှာ drift detected က true လား false လား?
ဘာကြောင့်လဲ? (လက်တွေ့မှာ synthetic data တူနေလို့ drift မရှိနိုင်ဘူး)

#### Task 8.4: Simulate Real Drift

တမင်တကာ different data နဲ့ drift ကိုဖန်တီးကြည့်ပါ:

```python
import numpy as np
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Reference: original training distribution
ref = pd.DataFrame({
    "amount": np.random.exponential(scale=500, size=1000),
    "oldbalanceOrg": np.random.exponential(scale=10000, size=1000),
    "newbalanceOrig": np.random.exponential(scale=9000, size=1000),
    "oldbalanceDest": np.random.exponential(scale=5000, size=1000),
    "newbalanceDest": np.random.exponential(scale=5500, size=1000),
})

# Current: drastically different distribution (simulating new customer base)
curr_drifted = pd.DataFrame({
    "amount": np.random.exponential(scale=50000, size=1000),  # 100x larger!
    "oldbalanceOrg": np.random.exponential(scale=1000000, size=1000),
    "newbalanceOrig": np.random.exponential(scale=950000, size=1000),
    "oldbalanceDest": np.random.exponential(scale=500, size=1000),  # 10x smaller!
    "newbalanceDest": np.random.exponential(scale=550, size=1000),
})

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=curr_drifted)
result = report.as_dict()

dr = result["metrics"][0]["result"]
print(f"Dataset drift: {dr['dataset_drift']}")
print(f"Drift score: {dr['share_of_drifted_columns']:.4f}")
print(f"Drifted features: {[c for c, v in dr.get('drift_by_columns', {}).items() if v.get('drift_detected')]}")

# Show detailed stats for each feature
for col, val in dr.get("drift_by_columns", {}).items():
    print(f"\n  {col}:")
    print(f"    Drift detected: {val.get('drift_detected')}")
    print(f"    KS statistic: {val.get('statistic', 0):.4f}")
    print(f"    p-value: {val.get('p_value', 0):.6f}")
    if val.get('drift_detected'):
        ref_dist = val.get('reference_distribution', {})
        curr_dist = val.get('current_distribution', {})
        if ref_dist:
            print(f"    Reference mean: {ref_dist.get('mean', 'N/A')}")
        if curr_dist:
            print(f"    Current mean: {curr_dist.get('mean', 'N/A')}")
```

**Q:** ဘယ် features တွေက drift ရှိတယ်လို့ပြောလဲ?
Distribution shift ရဲ့ပမာဏက drift detection ကိုဘယ်လိုသက်ရောက်လဲ?

#### Task 8.5: Gradual Drift Detection

```python
import numpy as np
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import matplotlib.pyplot as plt

# Reference distribution
ref = pd.DataFrame({
    "amount": np.random.normal(500, 200, 1000),
})

# Simulate gradual drift over 10 windows
drift_scores = []
for shift in np.linspace(0, 2000, 10):
    curr = pd.DataFrame({
        "amount": np.random.normal(500 + shift, 200, 1000),
    })
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref, current_data=curr)
    result = report.as_dict()
    dr = result["metrics"][0]["result"]
    is_drifted = any(
        v.get("drift_detected") 
        for v in dr.get("drift_by_columns", {}).values()
    )
    drift_scores.append({
        "shift": shift,
        "p_value": dr.get("drift_by_columns", {}).get("amount", {}).get("p_value", 1),
        "drift_detected": is_drifted,
    })

for s in drift_scores:
    marker = "⚠️" if s["drift_detected"] else "✅"
    print(f"{marker} Shift={s['shift']:6.1f}  p-value={s['p_value']:.4f}")
```

**Q:** Shift ဘယ်လောက်ရောက်မှ drift ကို detect လုပ်နိုင်လဲ?
Detection threshold ကို ဘယ်လိုချိန်ညှိနိုင်လဲ?

#### Task 8.6: Drift Response Strategy

Drift တွေ့ရင် ဘာလုပ်ရမလဲဆိုတာ discuss လုပ်ပါ:

```python
def handle_drift(drift_score, drifted_features, model_name):
    """Drift ကိုတွေ့ရင် ဘာလုပ်ရမလဲဆိုတဲ့ alert/action logic"""
    
    ALERTS = []
    
    if drift_score > 0.3:
        ALERTS.append(f"🔴 High drift detected ({drift_score:.1%} features)")
        ALERTS.append(f"   → Retrain model with new data")
        ALERTS.append(f"   → Route traffic to shadow model for comparison")
    
    if drift_score > 0.1:
        ALERTS.append(f"🟡 Moderate drift: notify data science team")
        ALERTS.append(f"   → Drifted features: {drifted_features}")
    
    if any(f in drifted_features for f in ["amount", "newbalanceOrig"]):
        ALERTS.append(f"⚡ Critical feature drifted: investigate immediately")
    
    if not ALERTS:
        ALERTS.append(f"✅ No action needed — model is stable")
    
    for alert in ALERTS:
        print(alert)
    
    return ALERTS

# Test cases
print("=== Severe Drift ===")
handle_drift(0.6, ["amount", "oldbalanceOrg", "newbalanceOrig"], "fraud-detector")

print("\n=== Moderate Drift ===")
handle_drift(0.2, ["oldbalanceDest"], "fraud-detector")

print("\n=== No Drift ===")
handle_drift(0.0, [], "fraud-detector")
```

### Verification Steps

- [ ] Evidently ကို import လုပ်လို့ရလား?
- [ ] Basic drift detection script အလုပ်လုပ်လား?
- [ ] collect_metrics run တဲ့အခါ drift ကို ES မှာ log လုပ်လား?
- [ ] Drift document မှာ `data_drift_score`, `drift_detected`, `drifted_features` ပါလား?
- [ ] Artificial drift က detect လုပ်လို့ရလား?
- [ ] Gradual drift က ဘယ် shift level မှာ detect လုပ်လဲ?

### Questions

1. Data drift နဲ့ concept drift ကွာခြားချက်ကဘာလဲ?
2. Evidently က KS test ကို ဘယ်လိုသုံးလဲ? p-value ကို ဘယ်လိုအဓိပ္ပါယ်ဖော်လဲ?
3. Drift threshold (0.3) ကို ဘာကြောင့်ဒီတန်ဖိုးထားတာလဲ?
4. Drift တွေ့ရင် ချက်ချင်း model ကို retrain လုပ်သင့်လား? ဘာကြောင့်လဲ?
5. Production မှာ reference data ကို ဘယ်လိုထိန်းသိမ်းထားသင့်လဲ?

---

## Lab 9: Docker & Containerization

### Learning Objectives

1. Dockerfile structure ကိုနားလည်ခြင်း
2. Multi-stage build ကိုသုံးတတ်ခြင်း
3. Container ကို build/run လုပ်တတ်ခြင်း
4. Container security best practices ကိုသိခြင်း

### Background Theory

#### 9.1 Docker Multi-stage Build ဆိုတာဘာလဲ?

Multi-stage build က **build အတွက်လိုအပ်တဲ့ tools တွေကို
runtime image ထဲမထည့်ဘဲ ခွဲထုတ်တဲ့နည်းပဲ။**

**ဘာကြောင့်သုံးလဲ?**

```
Single-stage build:
  python:3.11-slim + build-essential + gcc + all packages
  → Image size: ~500MB (build tools တွေပါနေလို့)

Multi-stage build:
  Stage 1: python:3.11-slim + build tools (compile packages)
  Stage 2: python:3.11-slim + compiled packages only
  → Image size: ~200MB (build tools တွေမပါတော့လို့)
```

#### 9.2 Dockerfile Instructions

| Instruction | Purpose | Our usage |
|-------------|---------|-----------|
| `FROM` | Base image | `python:3.11-slim` |
| `WORKDIR` | Working directory | `/app` |
| `COPY` | Copy files | `app/`, `model/` |
| `RUN` | Execute command | `pip install`, `apt-get` |
| `EXPOSE` | Declare port | `8080` |
| `USER` | Non-root user | `inference` |
| `HEALTHCHECK` | Container health | `curl /health` |
| `CMD` | Default command | `uvicorn main:app` |

#### 9.3 Container Security Best Practices

| Practice | ရှင်းလင်းချက် |
|----------|----------------|
| **Non-root user** | Root အနေနဲ့ app ကို run မထားဘူး |
| **Minimal base image** | `slim` variant ကို သုံးတယ် |
| **No build tools** | Compiler, debugger တွေ runtime မှာမပါဘူး |
| **Read-only filesystem** | Container filesystem ကို read-only ထားနိုင်တယ် |
| **Health check** | Docker/Swarm/orchestration က container health ကိုသိတယ် |

### Step-by-Step Tasks

#### Task 9.1: Analyze the Dockerfile

Dockerfile ကို အသေးစိတ်ဖတ်ပါ:

```dockerfile
# Line-by-line analysis

FROM python:3.11-slim AS builder
```
- Base image: `python:3.11-slim` (Debian-based, ~120MB)
- `AS builder` — Stage name သတ်မှတ်တယ်

```
WORKDIR /build
```
- Working directory သတ်မှတ်တယ်

```
COPY app/requirements.txt .
```
- ပထမဆုံး requirements.txt ကိုပဲ copy လုပ်တယ် (Layer caching)
- Code တွေကိုနောက်မှမှ copy လုပ်တယ်

```
RUN apt-get update && apt-get install -y build-essential libgomp1 && \
    pip install --no-cache-dir --user -r requirements.txt
```
- Build tools တွေ install လုပ်တယ်
- `--user` flag — system python ကိုမထိဘူး
- `--no-cache-dir` — pip cache မသိမ်းဘူး (image size ချွေတာ)

```
FROM python:3.11-slim
```
- Runtime stage — clean image

```
RUN groupadd -r inference && useradd -r -g inference inference
```
- Non-root user ဆောက်တယ်

```
COPY --from=builder /root/.local /root/.local
```
- Builder stage က packages တွေကို copy လုပ်တယ်

```
USER inference
```
- Root ကနေ inference user ကိုပြောင်းတယ်

```
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```
- Docker က container health ကို 30s တစ်ခါစစ်တယ်
- ၃ကြိမ်ဆက်တိုက်မအောင်ရင် container ကို restart လုပ်တယ်

**Q:** Layer caching က ဘယ်လိုအလုပ်လုပ်လဲ?
ဘာကြောင့် requirements.txt ကို code တွေမထည့်ခင် သီးသန့် copy လုပ်တာလဲ?

#### Task 9.2: Build the Docker Image

```bash
cd ml-inference

# Build with tag
docker build -t ml-inference:latest .

# Verify image exists
docker images ml-inference

# Check image size
docker images ml-inference --format "{{.Repository}}:{{.Tag}} {{.Size}}"
```

**Expected Output:**
```
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
ml-inference   latest    abc123def456   10 seconds ago   280MB
```

**Q:** Image size က ဘယ်လောက်လဲ? Base image (python:3.11-slim ~120MB) နဲ့ယှဉ်ရင်
ဘာတွေထပ်ပါလာလဲ?

#### Task 9.3: Run the Container

```bash
# Run container with environment variables
docker run -d --name ml-inference \
  -p 8080:8080 \
  -e MODEL_PATH=/app/model/model.pkl \
  -e ES_HOST=http://192.168.1.123:80 \
  -e ES_USER=elastic \
  -e ES_PASS=ML0psElk!2026 \
  ml-inference:latest

# Check container is running
docker ps

# Check logs
docker logs ml-inference

# Check health
docker inspect ml-inference --format "{{json .State.Health}}"
```

**Expected Health Status:**
```json
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [...]
}
```

#### Task 9.4: Test Containerized Server

```bash
# Health check
curl http://localhost:8080/health

# Prediction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'

# Verify ES log
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?size=1&sort=@timestamp:desc&pretty"
```

#### Task 9.5: Docker Security Check

```bash
# Check which user the container runs as
docker exec ml-inference whoami

# Check file permissions
docker exec ml-inference ls -la /app/
docker exec ml-inference ls -la /app/model/

# Try to write to filesystem (should fail or be limited)
docker exec ml-inference touch /tmp/test.txt
docker exec ml-inference touch /app/test.txt
```

**Q:** Container က root အနေနဲ့ run နေလား? inference user အနေနဲ့ run နေလား?
`/app` directory မှာ file ရေးလို့ရလား?

#### Task 9.6: Resource Limits

```bash
# Run with resource limits
docker run -d --name ml-inference-limited \
  -p 8081:8080 \
  --memory=256m \
  --cpus=1.0 \
  -e MODEL_PATH=/app/model/model.pkl \
  -e ES_HOST=http://192.168.1.123:80 \
  -e ES_USER=elastic \
  -e ES_PASS=ML0psElk!2026 \
  ml-inference:latest

# Check resource usage
docker stats ml-inference-limited --no-stream

# Test under load
for i in $(seq 1 50); do
  curl -s -X POST http://localhost:8081/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' > /dev/null
done
echo "50 requests completed"
```

**Q:** Memory 256MB နဲ့ CPU 1 core ဆိုရင် performance ဘယ်လိုရှိလဲ?
ပုံမှန် (unlimited) နဲ့ယှဉ်ရင် latency ကွာလား?

#### Task 9.7: Clean Up

```bash
# Stop and remove containers
docker stop ml-inference ml-inference-limited
docker rm ml-inference ml-inference-limited

# Remove image
docker rmi ml-inference:latest
```

### Verification Steps

- [ ] Docker build success (no errors)?
- [ ] `docker images` မှာ image ပေါ်လား?
- [ ] Image size က reasonable (200-300MB) လား?
- [ ] Container run success?
- [ ] Health check pass?
- [ ] Prediction success?
- [ ] Non-root user နဲ့ run နေလား?
- [ ] Resource limits အလုပ်လုပ်လား?

### Questions

1. ဘာကြောင့် `python:3.11-slim` ကို `python:3.11` (full) အစားသုံးတာလဲ?
2. Multi-stage build ရဲ့အားသာချက်တွေကဘာတွေလဲ?
3. Layer caching ကို optimize လုပ်ဖို့ Dockerfile ကိုဘယ်လိုပြောင်းလဲရေးသင့်လဲ?
4. Production မှာ container image ကို registry (ECR, Docker Hub) ပေါ်တင်ဖို့ ဘာတွေလိုအပ်လဲ?

---

## Lab 10: Production Hardening

### Learning Objectives

1. Secrets management ကိုနားလည်ခြင်း
2. Logging & monitoring ကိုတိုးတက်အောင်လုပ်ခြင်း
3. Error handling ကို strengthen လုပ်ခြင်း
4. Performance optimization လုပ်တတ်ခြင်း

### Background Theory

#### 10.1 Twelve-Factor App

ဒီ project က **12-Factor App** ရဲ့အချက်တွေကိုလိုက်နာထားတယ်:

| Factor | Implementation |
|--------|---------------|
| **III. Config** | Environment variables သုံးတယ် |
| **VI. Processes** | Stateless server (scale out) |
| **VII. Port binding** | Self-contained (uvicorn) |
| **XI. Logs** | Log events to stdout/stderr |

#### 10.2 Production Security Layers

```
Internet
   │
   ▼
┌─────────────┐
│  WAF/CloudFront │  Layer 1: DDoS protection, SSL termination
└─────────────┘
   │
   ▼
┌─────────────┐
│  API Gateway   │  Layer 2: Authentication, rate limiting, API keys
└─────────────┘
   │
   ▼
┌─────────────┐
│  ALB/Nginx    │  Layer 3: Load balancing, SSL, routing
└─────────────┘
   │
   ▼
┌─────────────┐
│  FastAPI App  │  Layer 4: Application logic
└─────────────┘
   │
   ▼
┌─────────────┐
│  ES (internal)│  Layer 5: Data storage (no public access)
└─────────────┘
```

### Step-by-Step Tasks

#### Task 10.1: Implement Structured Logging

```python
# Current: print() statements
# Better: structured logging (JSON)
import json
import logging

# Replace print with structured logging
class StructuredLogger:
    def __init__(self, name="ml-inference"):
        self.logger = logging.getLogger(name)
    
    def _log(self, level, event, **kwargs):
        record = {
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "service": "ml-inference",
            **kwargs
        }
        getattr(self.logger, level)(json.dumps(record))

logger = StructuredLogger()
logger._log("info", "model_loaded", model_path="/app/model/model.pkl", status="success")
logger._log("warn", "es_write_failed", error="connection refused", index="ml-inference")
```

**Q:** Structured logging ကဘာလို့အရေးကြီးလဲ?
(ELK stack နဲ့တွဲသုံးတဲ့အခါ parsing/search လုပ်ရတာလွယ်တယ်)

#### Task 10.2: Implement Retry with Backoff

```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """
    Retry a function with exponential backoff.
    
    Usage:
        retry_with_backoff(lambda: es.index(...))
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Last attempt failed
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
            print(f"[WARN] Attempt {attempt+1} failed: {e}. Retrying in {delay:.1f}s")
            time.sleep(delay)
    return None

# Usage in monitor.py
try:
    retry_with_backoff(
        lambda: self.es.index(index=self.inference_index, document=doc)
    )
except Exception as e:
    print(f"[ERROR] ES write failed after all retries: {e}")
```

**Q:** Exponential backoff ကဘာလို့အရေးကြီးလဲ?
(Server down ချိန်မှာ retry တွေက တစ်ပြိုင်နက်မရောက်အောင်)

#### Task 10.3: Add Request Rate Limiting

```python
# pip install slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.post("/predict")
@limiter.limit("100/minute")  # 100 requests per minute per IP
async def predict(request: Request, body: PredictRequest):
    ...
```

**Q:** Rate limiting ကဘာလို့လိုအပ်လဲ?
(Brute force attacks, accidental high traffic, cost control)

#### Task 10.4: Add Request Validation (Business Logic)

```python
from pydantic import validator

class PredictRequest(BaseModel):
    features: List[float]
    labels: Optional[List[str]] = None
    ground_truth: Optional[int] = None
    
    @validator("features")
    def validate_features(cls, v):
        if len(v) != 5:
            raise ValueError(f"Expected 5 features, got {len(v)}")
        if any(x < 0 for x in v):
            raise ValueError("Features cannot be negative")
        if any(not isinstance(x, (int, float)) for x in v):
            raise ValueError("All features must be numeric")
        return v
    
    @validator("ground_truth")
    def validate_ground_truth(cls, v):
        if v is not None and v not in [0, 1]:
            raise ValueError("Ground truth must be 0 or 1")
        return v
```

**Q:** Pydantic validator vs FastAPI middleware — ဘယ်အချိန်မှာဘယ်ဟာသုံးသင့်လဲ?

#### Task 10.5: Add Prometheus Metrics

```python
# The project already has prometheus-fastapi-instrumentator installed
# Let's add custom metrics

from prometheus_client import Counter, Histogram, Gauge

# Custom metrics
PREDICTIONS_TOTAL = Counter(
    "ml_predictions_total",
    "Total predictions",
    ["model_name", "label"]
)

PREDICTION_LATENCY = Histogram(
    "ml_prediction_latency_seconds",
    "Prediction latency in seconds",
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1]
)

MODEL_LOADED = Gauge(
    "ml_model_loaded",
    "Is model loaded (1=yes, 0=no)"
)

# In predict endpoint:
PREDICTIONS_TOTAL.labels(model_name="fraud-detector", label=label).inc()
PREDICTION_LATENCY.observe(total_ms / 1000)

# In health endpoint:
MODEL_LOADED.set(1 if model is not None else 0)
```

**Q:** Prometheus metrics vs ES metrics — ဘယ်အခြေအနေမှာဘယ်ဟာသုံးသင့်လဲ?

#### Task 10.6: Add Middleware for Request ID

```python
from fastapi import Request
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Add to response headers
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

**Q:** Request ID tracing ကဘာလို့အရေးကြီးလဲ?
(ELK / Distributed tracing တို့နဲ့တွဲသုံးတဲ့အခါ)

#### Task 10.7: Performance Test

```bash
# Simple load test using bash
echo "Testing with 100 concurrent requests..."

# Start time
START=$(date +%s%N)

# Send 100 requests in background
for i in $(seq 1 100); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' \
    -o /dev/null -w "%{http_code} %{time_total}\n" >> /tmp/results.txt &
done

# Wait for all to complete
wait

# Calculate stats
END=$(date +%s%N)
TOTAL_TIME=$(( ($END - $START) / 1000000 ))  # ms

# Show results
echo "Total time: ${TOTAL_TIME}ms"
echo "Throughput: $(( 100 * 1000 / $TOTAL_TIME )) req/sec"

# Show latency distribution
awk '{print $2}' /tmp/results.txt | sort -n | awk '
  BEGIN {count=0}
  {vals[count++]=$1}
  END {
    print "Min latency: " vals[0] "s"
    print "P50 latency: " vals[int(count*0.5)] "s"
    print "P90 latency: " vals[int(count*0.9)] "s"
    print "P95 latency: " vals[int(count*0.95)] "s"
    print "P99 latency: " vals[int(count*0.99)] "s"
    print "Max latency: " vals[count-1] "s"
  }
'

rm -f /tmp/results.txt
```

### Verification Steps

- [ ] Structured logging test pass?
- [ ] Retry with backoff implementation?
- [ ] Rate limiting test pass?
- [ ] Validator functions work?
- [ ] Prometheus metrics at `/metrics`?
- [ ] Request ID in response headers?
- [ ] 100 concurrent requests complete without errors?

### Questions

1. Production အတွက် အရေးကြီးဆုံး hardening က ဘာလဲ?
2. Security vs performance — ဘယ်လို balance လုပ်မလဲ?
3. ဒီ project ကို production မှာ run ဖို့ အနည်းဆုံးဘာတွေထပ်လိုအပ်လဲ?
4. MONitoring (observability) အတွက် ဘာ tools တွေထပ်သုံးသင့်လဲ? (ELK, Grafana, Prometheus, Jaeger)

---

## Appendix A: Quick Reference

### Common Commands

```bash
# Train model
python -m app.train_model

# Run server
uvicorn main:app --host 0.0.0.0 --port 8080

# Run metrics
python -m app.collect_metrics

# Build Docker
docker build -t ml-inference:latest .

# Run Docker
docker run -d -p 8080:8080 ml-inference:latest
```

### ES Queries

```bash
# Check connection
curl -u elastic:'ML0psElk!2026' http://192.168.1.123:80

# View indices
curl -u elastic:'ML0psElk!2026' http://192.168.1.123:80/_cat/indices/ml-*?v

# Search latest prediction
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?size=1&sort=@timestamp:desc"
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `/app/model/model.pkl` | Path to model.pkl |
| `ES_HOST` | `http://192.168.1.123:80` | Elasticsearch URL |
| `ES_USER` | `elastic` | ES username |
| `ES_PASS` | `ML0psElk!2026` | ES password |
| `MODEL_NAME` | `fraud-detector` | Model identifier |
| `MODEL_VERSION` | `1.0.0` | Model version |
| `NAMESPACE` | `ml-inference` | orchestration namespace |
| `POD_NAME` | `unknown` | orchestration pod name |
| `ENVIRONMENT` | `production` | Environment label |

---

*End of Lab Exercises*

---

## Appendix B: Additional Lab Exercises (Advanced)

### Lab B1: Custom Model Deployment

**Objective:** Create a new model (Random Forest) and serve it alongside GradientBoosting.

**Steps:**
1. Create `app/train_rf_model.py` that trains a RandomForestClassifier
2. Save it as `model/rf_model.pkl`
3. Modify `main.py` to load both models
4. Add endpoint `POST /predict/{model_name}` to select model
5. Compare prediction results between models

**Verification:**
```bash
curl -X POST http://localhost:8080/predict/gradient_boosting \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'

curl -X POST http://localhost:8080/predict/random_forest \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
```

**Questions:**
- Do both models predict the same label for the same input?
- Which model has faster inference time?
- Which model has a smaller file size?

---

### Lab B2: Real-time Dashboard with Kibana

**Objective:** Create a Kibana dashboard to visualize inference metrics.

**Steps:**
1. Go to Kibana (http://192.168.1.123:5601 or your Kibana URL)
2. Create Data View for `ml-inference` index
3. Create visualizations:
   - Bar chart: predictions over time (date histogram)
   - Pie chart: fraud vs non-fraud distribution
   - Metric: average latency
   - Data table: latest 10 predictions
4. Create a dashboard combining all visualizations

**Verification:**
- Make 20+ predictions from different terminals
- Refresh Kibana dashboard
- Data should update in real-time (with 30s ES refresh interval)

**Questions:**
- What is the refresh interval for the ES index?
- Can you see latency spikes in the dashboard?
- How would you set up a threshold alert in Kibana?

---

### Lab B3: Adding Request Caching

**Objective:** Cache frequent predictions to reduce latency.

**Steps:**
1. Install `cachetools`: `pip install cachetools`
2. Add LRU cache to predict endpoint:

```python
from cachetools import LRUCache, cached
from hashlib import sha256

cache = LRUCache(maxsize=1000)

def get_cache_key(features):
    return sha256(str(features).encode()).hexdigest()

@app.post("/predict")
async def predict(request: Request, body: PredictRequest):
    cache_key = get_cache_key(body.features)
    
    if cache_key in cache:
        print(f"[CACHE HIT] {cache_key}")
        return cache[cache_key]
    
    result = await predict_internal(body)
    cache[cache_key] = result
    print(f"[CACHE MISS] {cache_key}")
    return result
```

**Verification:**
- Send the same request twice
- First request: cache miss, full inference
- Second request: cache hit, ~0.01ms response
- Latency should drop from ~0.7ms to ~0.01ms

**Questions:**
- When would caching be dangerous? (hint: model updates)
- How do you invalidate the cache when the model changes?
- What is a good maxsize for your LRU cache?

---

### Lab B4: Model Versioning with Canary Testing

**Objective:** Deploy two model versions and route traffic between them.

**Steps:**
1. Train a second model with different parameters (e.g., n_estimators=50)
2. Save as `model/model_v2.pkl`
3. Create a model registry in `main.py`:

```python
MODELS = {
    "v1.0.0": joblib.load("model/model.pkl"),
    "v1.1.0": joblib.load("model/model_v2.pkl"),
}
```

4. Implement traffic splitting:

```python
import random

def get_model_version():
    """90% v1.0.0, 10% v1.1.0 (canary)"""
    return "v1.1.0" if random.random() < 0.1 else "v1.0.0"
```

5. Log which version served each request in the ES document

**Verification:**
- Send 100 requests in a loop
- Check ES for model_version distribution (~90 v1.0.0, ~10 v1.1.0)
- Compare latency between versions

**Questions:**
- What metrics would you monitor during a canary test?
- At what point would you promote the canary to 100%?
- How do you rollback if the canary shows problems?

---

### Lab B5: API Gateway Integration

**Objective:** Add authentication and rate limiting at the gateway level.

**Steps:**
1. Install `slowapi`: `pip install slowapi`
2. Add to `main.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.post("/predict")
@limiter.limit("10/second")
async def predict(request: Request, body: PredictRequest):
    # existing code...
```

3. Create a simple API key check:

```python
API_KEYS = {"key1": "user1", "key2": "user2"}

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path in ["/health", "/ready", "/docs", "/openapi.json"]:
        return await call_next(request)
    api_key = request.headers.get("X-API-Key")
    if api_key not in API_KEYS:
        raise HTTPException(401, detail="Invalid API key")
    return await call_next(request)
```

**Verification:**
```bash
# Without API key — should get 401
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'

# With wrong API key — should get 401
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wrong-key" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'

# With correct API key — should succeed
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: key1" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'

# Rate limit test (11 requests in 1 second)
for i in $(seq 1 11); do
  curl -s -o /dev/null -w "%{http_code} " \
    -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -H "X-API-Key: key1" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
done
echo ""
# Expected: 200 200 200 ... 200 429 (last one rate limited)
```

**Questions:**
- API key vs JWT token — which is more secure?
- How do you securely store API keys in production?
- What rate limits make sense for your use case?

---

### Lab B6: Performance Load Testing

**Objective:** Measure server performance under different load conditions.

**Steps:**
1. Install `locust`: `pip install locust`
2. Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class InferenceUser(HttpUser):
    wait_time = between(0.5, 2.0)
    
    @task
    def predict_normal(self):
        self.client.post("/predict", json={
            "features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]
        })
    
    @task(2)  # 2x more likely
    def predict_fraud(self):
        self.client.post("/predict", json={
            "features": [99999.0, 500000.0, 0.0, 100.0, 100100.0]
        })
```

3. Run locust:
```bash
locust -f locustfile.py --host=http://localhost:8080 --users=10 --spawn-rate=1
```

4. Open browser to http://localhost:8089
5. Start with 10 users, ramp up to 100
6. Record results:
   - Requests per second
   - P50/P95/P99 latency
   - Error rate
   - CPU/memory usage

**Expected Results (estimate):**
| Users | Throughput | P50 Latency | P99 Latency | Error Rate |
|-------|-----------|-------------|-------------|------------|
| 10 | 50 req/s | 2ms | 5ms | 0% |
| 50 | 200 req/s | 5ms | 20ms | 0% |
| 100 | 300 req/s | 15ms | 100ms | 0.1% |
| 200 | 400 req/s | 50ms | 500ms | 1% |

**Questions:**
- At what point does latency become unacceptable (>1s p99)?
- What is the bottleneck — CPU, memory, or I/O?
- How many workers would you need for 1000 req/s?

---

### Lab B7: Feature Store Integration

**Objective:** Instead of requiring clients to send all 5 features, compute some from a feature store.

**Steps:**
1. Create a simple in-memory feature store (simulating Redis/Feast):

```python
class FeatureStore:
    def __init__(self):
        self._store = {}
    
    def get_account_features(self, account_id):
        """Simulate fetching features from a store"""
        if account_id in self._store:
            return self._store[account_id]
        # Simulate default values
        return {
            "oldbalanceOrg": 10000.0,
            "oldbalanceDest": 5000.0,
        }
    
    def update_balance(self, account_id, balance):
        self._store[account_id] = balance
```

2. Create a new endpoint that accepts minimal input:

```python
class PredictWithContextRequest(BaseModel):
    amount: float
    sender_id: str
    receiver_id: str

@app.post("/predict_with_context")
async def predict_with_context(body: PredictWithContextRequest):
    sender = feature_store.get_account_features(body.sender_id)
    receiver = feature_store.get_account_features(body.receiver_id)
    
    features = [
        body.amount,
        sender["oldbalanceOrg"],
        sender["oldbalanceOrg"] - body.amount,  # newbalanceOrig
        receiver["oldbalanceDest"],
        receiver["oldbalanceDest"] + body.amount,  # newbalanceDest
    ]
    
    X = np.array(features).reshape(1, -1)
    label_index = int(model.predict(X)[0])
    return {"prediction": label_index, "features_used": features}
```

**Verification:**
```bash
curl -X POST http://localhost:8080/predict_with_context \
  -H "Content-Type: application/json" \
  -d '{"amount": 500.0, "sender_id": "user_123", "receiver_id": "merchant_456"}'
```

**Questions:**
- How would you implement this with a real feature store like Redis or Feast?
- What are the latency implications of fetching features from an external store?
- How do you handle missing features in production?

---

### Lab B8: Drift Alerting with Webhooks

**Objective:** Send a Slack/Telegram notification when drift is detected.

**Steps:**
1. Create `app/alerter.py`:

```python
import requests
import os

SLACK_WEBHOOK_URL=os.get...RL", "")
TELEGRAM_BOT_TOKEN=os.get...EN", "")
TELEGRAM_CHAT_ID=os.get...AT_ID", "")

def send_slack_alert(message):
    if not SLACK_WEBHOOK_URL:
        return
    requests.post(SLACK_WEBHOOK_URL, json={"text": message})

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def alert_drift(drift_score, drifted_features, model_name):
    message = (
        f"🚨 ML Drift Alert\n"
        f"Model: {model_name}\n"
        f"Drift Score: {drift_score:.2%}\n"
        f"Drifted Features: {', '.join(drifted_features)}\n"
        f"Time: {datetime.now(timezone.utc).isoformat()}"
    )
    send_slack_alert(message)
    send_telegram_alert(message)
    print(message)
```

2. Integrate into `collect_metrics.py`:

```python
if dr.get("dataset_drift", False):
    alert_drift(
        drift_score=dr.get("share_of_drifted_columns", 0),
        drifted_features=drifted,
        model_name=monitor.model_name
    )
```

**Verification:**
- Run collect_metrics after making predictions with drifted data
- Check if Slack/Telegram received the alert
- Test with artificial drift (different distribution data)

**Questions:**
- What alert severity levels would you define for different drift scores?
- How do you prevent alert fatigue (too many alerts)?
- What is the appropriate response time for drift alerts?

---

### Lab B9: A/B Testing Analysis

**Objective:** Compare two model versions statistically.

**Steps:**
1. Create `app/ab_test.py`:

```python
import numpy as np
from scipy import stats

def analyze_ab_test(control_results, treatment_results):
    """
    control_results: list of dicts with latency, accuracy, etc.
    treatment_results: same format
    """
    # Latency comparison (t-test)
    t_stat, p_value = stats.ttest_ind(
        [r["latency_ms"] for r in control_results],
        [r["latency_ms"] for r in treatment_results]
    )
    
    print(f"Latency Comparison:")
    print(f"  Control mean:    {np.mean([r['latency_ms'] for r in control_results]):.3f}ms")
    print(f"  Treatment mean:  {np.mean([r['latency_ms'] for r in treatment_results]):.3f}ms")
    print(f"  T-statistic:     {t_stat:.4f}")
    print(f"  P-value:         {p_value:.4f}")
    print(f"  Significant:     {'YES' if p_value < 0.05 else 'NO'}")
    
    # Accuracy comparison (proportion test)
    from statsmodels.stats.proportion import proportions_ztest
    
    control_correct = sum(1 for r in control_results if r["correct"])
    treatment_correct = sum(1 for r in treatment_results if r["correct"])
    
    counts = np.array([control_correct, treatment_correct])
    nobs = np.array([len(control_results), len(treatment_results)])
    
    z_stat, p_value = proportions_ztest(counts, nobs)
    
    print(f"\nAccuracy Comparison:")
    print(f"  Control:   {control_correct}/{len(control_results)} = {control_correct/len(control_results):.2%}")
    print(f"  Treatment: {treatment_correct}/{len(treatment_results)} = {treatment_correct/len(treatment_results):.2%}")
    print(f"  Z-statistic: {z_stat:.4f}")
    print(f"  P-value:     {p_value:.4f}")
    print(f"  Significant: {'YES' if p_value < 0.05 else 'NO'}")
```

**Verification:**
- Collect 100+ predictions from each model version
- Run the analysis script
- Determine if the new model is statistically better

**Questions:**
- What sample size do you need for statistically significant results?
- P-value < 0.05 means what exactly?
- What business metrics matter beyond accuracy and latency?

---

### Lab B10: Full MLOps Pipeline Simulation

**Objective:** Create a script that simulates the complete ML lifecycle.

**Steps:**
1. Create `app/ml_pipeline.py`:

```python
"""
Simulates the complete ML lifecycle:
1. Data collection → 2. Training → 3. Validation → 
4. Deployment → 5. Monitoring → 6. Retrain decision
"""
import time
import numpy as np
from datetime import datetime, timezone

class MLPipeline:
    def __init__(self):
        self.stages = []
        self.start_time = None
    
    def stage(self, name, func):
        """Run a pipeline stage with timing"""
        t0 = time.perf_counter()
        print(f"\n{'='*60}")
        print(f"🔄 Stage: {name}")
        print(f"{'='*60}")
        try:
            result = func()
            elapsed = (time.perf_counter() - t0) * 1000
            self.stages.append({"name": name, "status": "PASS", "time_ms": elapsed})
            print(f"✅ {name} completed in {elapsed:.1f}ms")
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - t0) * 1000
            self.stages.append({"name": name, "status": "FAIL", "time_ms": elapsed})
            print(f"❌ {name} FAILED: {e}")
            raise
    
    def run(self):
        self.start_time = time.perf_counter()
        
        # Stage 1: Data Collection
        def collect_data():
            # Simulate receiving 1000 new transactions
            data = np.random.randn(1000, 5)
            labels = np.random.choice([0, 1], 1000, p=[0.99, 0.01])
            print(f"  Collected {len(data)} transactions ({labels.mean()*100:.2f}% fraud)")
            return data, labels
        
        # Stage 2: Data Validation
        def validate_data(data):
            assert not np.any(np.isnan(data)), "NaN values detected!"
            assert data.shape[1] == 5, f"Expected 5 features, got {data.shape[1]}"
            print(f"  Data validation passed: shape={data.shape}, range=[{data.min():.2f}, {data.max():.2f}]")
            return True
        
        # Stage 3: Training
        def train_model():
            from sklearn.ensemble import GradientBoostingClassifier
            from sklearn.preprocessing import RobustScaler
            from sklearn.pipeline import Pipeline
            
            X = np.random.randn(5000, 5)
            y = np.random.choice([0, 1], 5000, p=[0.99, 0.01])
            
            model = Pipeline([
                ("scaler", RobustScaler()),
                ("classifier", GradientBoostingClassifier(n_estimators=50, random_state=42)),
            ])
            model.fit(X, y)
            acc = model.score(X, y)
            print(f"  Model trained: accuracy={acc:.4f}")
            return model
        
        # Stage 4: Validation
        def validate_model(model):
            X_test = np.random.randn(1000, 5)
            y_test = np.random.choice([0, 1], 1000, p=[0.99, 0.01])
            acc = model.score(X_test, y_test)
            print(f"  Test accuracy: {acc:.4f}")
            if acc < 0.9:
                raise ValueError(f"Accuracy too low: {acc:.4f}")
            return acc
        
        # Stage 5: Deployment
        def deploy():
            print(f"  Deploying model to production...")
            time.sleep(0.5)  # Simulate deployment time
            print(f"  Model deployed at {datetime.now(timezone.utc).isoformat()}")
            return True
        
        # Stage 6: Monitoring simulation
        def monitor():
            print(f"  Monitoring model in production...")
            time.sleep(0.3)
            # Simulate drift detection
            if np.random.random() < 0.3:  # 30% chance of drift
                print(f"  ⚠️ Data drift detected! Score: {np.random.random():.2f}")
                return "DRIFT_DETECTED"
            print(f"  ✅ No drift detected")
            return "STABLE"
        
        # Execute stages
        data, labels = self.stage("Data Collection", collect_data)
        self.stage("Data Validation", lambda: validate_data(data))
        model = self.stage("Model Training", train_model)
        acc = self.stage("Model Validation", lambda: validate_model(model))
        self.stage("Deployment", deploy)
        status = self.stage("Monitoring", monitor)
        
        # Summary
        total_time = (time.perf_counter() - self.start_time) * 1000
        print(f"\n{'='*60}")
        print(f"📊 PIPELINE SUMMARY")
        print(f"{'='*60}")
        print(f"Total time: {total_time:.0f}ms")
        print(f"Stages: {len(self.stages)}")
        for s in self.stages:
            print(f"  {'✅' if s['status']=='PASS' else '❌'} {s['name']:25s} {s['time_ms']:8.1f}ms")
        
        if status == "DRIFT_DETECTED":
            print(f"\n🔄 Triggering retrain pipeline...")
        
        return {"status": status, "accuracy": float(acc)}

if __name__ == "__main__":
    pipeline = MLPipeline()
    result = pipeline.run()
    print(f"\nFinal result: {result}")
```

**Verification:**
```bash
cd ml-inference
python -m app.ml_pipeline
```

**Expected Output:**
```
============================================================
🔄 Stage: Data Collection
============================================================
  Collected 1000 transactions (0.90% fraud)
✅ Data Collection completed in 2.3ms

============================================================
🔄 Stage: Data Validation
============================================================
  Data validation passed
✅ Data Validation completed in 1.1ms

... (continues through all stages)

============================================================
📊 PIPELINE SUMMARY
============================================================
Total time: 2150ms
Stages: 6
  ✅ Data Collection            2.3ms
  ✅ Data Validation            1.1ms
  ✅ Model Training           850.0ms
  ✅ Model Validation          45.0ms
  ✅ Deployment               502.0ms
  ✅ Monitoring               301.0ms
```

**Questions:**
- How would you integrate this with a real CI/CD pipeline (GitHub Actions)?
- What stages are missing from this simulation?
- How do you handle pipeline failures (retry, rollback, alert)?

---

*End of Lab Exercises — Additional Labs*

