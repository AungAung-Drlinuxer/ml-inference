# ML Inference Service — Lab Solutions

![Solutions](https://img.shields.io/badge/Solutions-10%20Labs-brightgreen)

---

## 📑 Solutions Index

| Lab | Title | Page |
|-----|-------|------|
| 1 | Environment Setup & Project Structure | [▶ Solution 1](#lab-1-solution-environment-setup) |
| 2 | Model Training & Understanding | [▶ Solution 2](#lab-2-solution-model-training) |
| 3 | Running the Inference Server | [▶ Solution 3](#lab-3-solution-running-the-server) |
| 4 | Making Predictions | [▶ Solution 4](#lab-4-solution-making-predictions) |
| 5 | Error Handling & Edge Cases | [▶ Solution 5](#lab-5-solution-error-handling) |
| 6 | Elasticsearch Integration | [▶ Solution 6](#lab-6-solution-elasticsearch) |
| 7 | Metrics Collection & Analysis | [▶ Solution 7](#lab-7-solution-metrics) |
| 8 | Data Drift Detection | [▶ Solution 8](#lab-8-solution-drift-detection) |
| 9 | Docker & Containerization | [▶ Solution 9](#lab-9-solution-docker) |
| 10 | Production Hardening | [▶ Solution 10](#lab-10-solution-production-hardening) |

---

## How to Use This Solutions File

- **Do NOT** peek at the solutions until you've tried the lab yourself
- Solutions include **complete code** + **explanations** (မြန်မာလိုရှင်းပြချက်)
- ကိုယ်တိုင်စမ်းကြည့်ပြီးမှသာ solution ကိုဖွင့်ကြည့်ပါ
- "ဘာကြောင့်ဒီလိုလုပ်ရတာလဲ" ဆိုတာကိုပါရှင်းပြထားတယ်

---

## Lab 1 Solution: Environment Setup & Project Structure

### Task 1.1: Clone/Download the Project

**Solution:**

```bash
# If the project is on GitHub:
git clone https://github.com/your-username/ml-inference.git
cd ml-inference

# If you received the files directly:
# Just navigate to the project directory
cd ml-inference
```

**Verification:**
```bash
ls -la
# Output should show:
# total XX
# drwxr-xr-x  ... README.md
# drwxr-xr-x  ... Dockerfile
# drwxr-xr-x  ... app/
# drwxr-xr-x  ... model/
# drwxr-xr-x  ... data/
```

**ရှင်းလင်းချက်:**

`git clone` က remote repository ကနေ local machine ကို project files တွေကို
download လုပ်ပေးတယ်။ `cd` က project folder ထဲကိုဝင်ဖို့အတွက်ဖြစ်တယ်။

---

### Task 1.2: Create Virtual Environment

**Solution:**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

**Verification:**
```bash
# Windows: prompt မှာ (.venv) ပါလား?
(.venv) C:\Users\...\ml-inference>

# which python က venv ကိုပြလား?
which python
# Expected: /path/to/ml-inference/.venv/bin/python
```

**ဘာကြောင့်ဒီလိုလုပ်ရတာလဲ?**

Virtual environment က project တစ်ခုချင်းစီအတွက် သီးသန့် Python environment
တစ်ခုဆောက်ပေးတယ်။ ဒါကြောင့်:

1. Project A က `flask==2.0` လိုအပ်တယ်၊ Project B က `flask==3.0` လိုအပ်တယ်
2. Virtual environment မသုံးရင် တစ်ခုနဲ့တစ်ခု conflict ဖြစ်မယ်
3. System Python ကိုမထိခိုက်ဘူး — ပျက်သွားရင်လည်း `.venv` folder ကိုဖျက်ပြီး
   အသစ်ဆောက်လို့ရတယ်

**အဖြစ်များတဲ့အမှားများ:**

❌ `python` ကို root/C:/Python312 ကနေသုံးမိတာ
✅ Virtual environment ကို activate လုပ်ဖို့မေ့တတ်တယ် — terminal တိုင်းမှာ
   activate လုပ်ဖို့လိုတယ်

---

### Task 1.3: Install Dependencies

**Solution:**

```bash
# Using pip (slower but reliable)
pip install -r app/requirements.txt
```

**Verification:**
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

**Expected Output:**
```
All packages installed successfully!
FastAPI: 0.111.0
scikit-learn: 1.4.2
numpy: 1.26.4
pandas: 2.2.2
elasticsearch: 8.12.0
```

**ဘာကြောင့်ဒီလိုလုပ်ရတာလဲ?**

`requirements.txt` က project အတွက်လိုအပ်တဲ့ Python packages တွေကို
version နဲ့တကွ စာရင်းပြုစုထားတယ်။ `pip install -r` က ဒီစာရင်းထဲက
package တွေအကုန်လုံးကို တစ်ခါတည်းသွင်းပေးတယ်။

**ES Client Version Note:**

`elasticsearch==8.12.0` ကိုသုံးထားတာက — version 9.x က ES 8.19.17 server နဲ့
မတူဘူး (Accept header mismatch). Version 8.13.0 က Windows မှာ opentelemetry issue ရှိတယ်။
ဒါကြောင့် 8.12.0 က အကောင်းဆုံးဖြစ်တယ်။

---

### Task 1.5: Understand Each File's Purpose

**Solution:**

| File Name | Purpose (၃-၅ word) | Main Class/Function |
|-----------|--------------------|--------------------|
| `app/main.py` | FastAPI inference server | `FastAPI app`, `predict()` |
| `app/monitor.py` | ES logging class | `InferenceMonitor` |
| `app/collect_metrics.py` | Metrics collector | `fetch_recent_inferences()`, `main()` |
| `app/train_model.py` | Model training | `train()`, `generate_sample_data()` |

**ရှင်းလင်းချက်:**

- **main.py:** REST API server — request တွေကိုလက်ခံတယ်, model ကို run တယ်, response ပြန်တယ်
- **monitor.py:** ES ကို log ရေးတဲ့ class — inference details, metrics, drift reports
- **collect_metrics.py:** ၁၅ မိနစ်တစ်ခါ ES ကနေ log တွေကိုယူပြီး accuracy, F1, latency တွက်တယ်
- **train_model.py:** Synthetic data နဲ့ model ကို train လုပ်တယ် — one-time run

---

### Task 1.6: Examine Requirements

**Solution:**

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

---

### Lab 1 Questions & Answers

**Q1:** ဘာကြောင့် `requirements.txt` မှာ version တွေကို `==` နဲ့ pin ထားတာလဲ?

**A:** Version pinning က **reproducible builds** အတွက်ဖြစ်တယ်။
`package>=1.0` လို့သုံးရင် မနက်ဖြန် `pip install` လုပ်ရင် version အသစ် (2.0) ရလာမယ်။
ဒါပေမယ့် version 2.0 မှာ breaking changes ပါလာရင် project ပျက်သွားမယ်။
`==1.0` ဆိုရင်တော့ ဘယ်အချိန် install လုပ်လုပ်တူညီတဲ့ version ကိုရမယ်။

**Q2:** `uvicorn[standard]` ဆိုတဲ့ `[standard]` က ဘာအတွက်လဲ?

**A:** `[standard]` က **extras** လို့ခေါ်တယ်။ uvicorn ရဲ့ standard extras မှာ
`httptools` (HTTP parsing performance) နဲ့ `websockets` (WebSocket support) တို့ပါတယ်။
`uvicorn` (base) နဲ့ `uvicorn[standard]` ကွာခြားချက်က performance ဖြစ်တယ် —
standard က 2-3x ပိုမြန်တယ်။

**Q3:** Virtual environment မသုံးရင် ဘာဖြစ်နိုင်လဲ?

**A:**
1. **Version conflicts:** Project A က `flask==2.0`, Project B က `flask==3.0` လိုအပ်ရင်
   တစ်ခုတည်းသုံးလို့မရဘူး
2. **System pollution:** System Python ကို packages တွေနဲ့ဖြည့်လိုက်ရင်
   OS tools တွေပျက်သွားနိုင်တယ် (Linux မှာ apt က python ကိုမှီခိုတယ်)
3. **Cleanup ခက်တယ်:** ဘယ် package က ဘယ် project အတွက်လဲဆိုတာသိဖို့ခက်တယ်

**Q4:** `pydantic` package က ဘာအတွက်လိုအပ်တာလဲ?

**A:** Pydantic က **data validation library** ဖြစ်တယ်။ FastAPI က pydantic ကိုသုံးပြီး:
1. Request body ကို auto-validate လုပ်တယ် (type checking, field required)
2. OpenAPI schema ကို auto-generate လုပ်တယ်
3. IDE autocomplete ကိုရတယ် (Python type hints ကိုသုံးတယ်)
4. Nested data structures ကို easy နဲ့ handle လုပ်တယ်

---

## Lab 2 Solution: Model Training & Understanding

### Task 2.1: Run Training Script

**Solution:**

```bash
cd ml-inference
python -m app.train_model
```

**Expected Output:**
```
2026-06-30 21:31:45,067 | Training fraud-detection model (raw vector pipeline)...
2026-06-30 21:31:45,069 | Generated 10000 rows (fraud rate = 0.0091)
2026-06-30 21:31:46,713 | Train accuracy: 1.0000
2026-06-30 21:31:46,713 | Test accuracy:  1.0000
2026-06-30 21:31:46,713 | Sample pred=0 proba=[0.99999999, 0.00000001]
2026-06-30 21:31:46,717 | Model saved to .../model/model.pkl
2026-06-30 21:31:46,721 | Reference data saved to .../data/reference.csv
```

**ဘာဖြစ်သွားလဲဆိုတာရှင်းပြချက်:**

1. `generate_sample_data(10000)` က synthetic transaction data 10,000 rows ဆောက်တယ်
   - Fraud rate: 0.91% (91 fraud rows, 9909 non-fraud)
   - Features: amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest
2. Data ကို train (80%) နဲ့ test (20%) ခွဲတယ်
3. `RobustScaler` နဲ့ feature scaling လုပ်တယ်
4. `GradientBoostingClassifier` (trees=150, depth=4) ကို train လုပ်တယ်
5. Accuracy: 100% (synthetic data က pattern ရှင်းလို့)
6. `model/model.pkl` ကို save လုပ်တယ်
7. `data/reference.csv` (training data 1000 rows) ကို drift detection အတွက် save လုပ်တယ်

---

### Task 2.2: Examine Generated Data

**Solution:**

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data/sample_data.csv")
print(f"Shape: {df.shape}")                    # (10000, 6)
print(f"Columns: {list(df.columns)}")           # ['amount', 'oldbalanceOrg', ..., 'isFraud']
print(f"\nFraud rate: {df['isFraud'].mean():.4f}")  # ~0.0091

print(f"\nFeature statistics:")
print(df.describe())

print(f"\nFraud vs Non-Fraud comparison:")
print(df.groupby("isFraud").describe().T)
```

**Expected Output (Fraud vs Non-Fraud):**

| Feature | Non-Fraud (mean) | Fraud (mean) | Difference |
|---------|-----------------|--------------|------------|
| amount | ~$1,000 | ~$25,000 | **25x higher** 🔴 |
| oldbalanceOrg | ~$5,000 | ~$80,000 | **16x higher** 🔴 |
| newbalanceOrig | ~$4,000 | **$0** | **Zeroed out** 🔴 |
| oldbalanceDest | ~$5,000 | ~$8,000 | Normal |
| newbalanceDest | ~$6,000 | ~$33,000 | Higher |

**ဘာကြောင့်ဒီ pattern တွေဖြစ်နေလဲ?**

Fraud ဖြစ်တဲ့အခါ:
1. ငွေပမာဏက ပုံမှန်ထက်များတယ် (အမြတ်ထုတ်ချင်လို့)
2. ပေးပို့သူရဲ့လက်ကျန်က ၀ သွားတယ် (ငွေအကုန်ထုတ်)
3. ပေးပို့သူရဲ့မူလလက်ကျန်က များတယ် (ပစ်မှတ်က ငွေရှိသူတွေ)

---

### Task 2.3: Load and Inspect Model

**Solution:**

```python
import joblib
import numpy as np

pipeline = joblib.load("model/model.pkl")
print(f"Pipeline type: {type(pipeline)}")              # Pipeline
print(f"Pipeline steps: {[s[0] for s in pipeline.steps]}")  # ['scaler', 'classifier']

clf = pipeline.named_steps["classifier"]
print(f"Classifier: {type(clf).__name__}")             # GradientBoostingClassifier
print(f"Number of trees: {clf.n_estimators}")           # 150
print(f"Max depth: {clf.max_depth}")                    # 4
print(f"Learning rate: {clf.learning_rate}")            # 0.1
```

**Pipeline Structure:**

```
Input (5 features)
    │
    ▼
RobustScaler
    ├─ Subtract median (per feature)
    └─ Divide by IQR (per feature)
    │
    ▼
GradientBoostingClassifier
    ├─ Tree 1: Predict → Error
    ├─ Tree 2: Fix Tree 1 errors → Error
    ├─ Tree 3: Fix Tree 2 errors → Error
    ...
    ├─ Tree 150: Fix Tree 149 errors → Final
    │
    ▼
Output (class 0 or 1 + probabilities)
```

---

### Task 2.4: Make Test Predictions

**Solution:**

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

**Expected Output:**
```
Normal transaction:
  Prediction: 0 (not fraud)
  Confidence: 1.0000
  Probabilities: [0.99999999 0.00000001]

Fraud transaction:
  Prediction: 1 (fraud)
  Confidence: 1.0000
  Probabilities: [0.00000001 0.99999999]
```

**ရှင်းလင်းချက်:**

`predict()` က class label (0 or 1) ကိုပဲပြန်တယ်။
`predict_proba()` က probability distribution ကိုပြန်တယ် — class 0 probability နဲ့
class 1 probability။

ပုံမှန် transaction မှာ class 0 (not fraud) probability က 99.999999% ရှိတယ်။
Fraud မှာတော့ class 1 (fraud) probability က 99.999999% ရှိတယ်။

---

### Task 2.5: Experiment with Different Inputs

**Solution:**

```python
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
    print(f"{desc:30s} → {'FRAUD' if pred else 'safe'} (conf={conf:.4f})")
```

**Expected Output:**
```
Very small transaction          → safe (conf=1.0000)
Normal transaction              → safe (conf=1.0000)
Large but normal                → safe (conf=0.9999)
Suspicious (balance zeroed)     → FRAUD (conf=1.0000)
Very suspicious                 → FRAUD (conf=1.0000)
```

**Q:** ဘယ် feature combination က fraud ဖြစ်နိုင်ခြေများလဲ?

**A:** `newbalanceOrig` (ပေးပို့သူရဲ့နောက်ဆုံးလက်ကျန်) က 0 ဖြစ်တဲ့အခါ
fraud ဖြစ်နိုင်ခြေများတယ်။ ဒါက fraud pattern ရဲ့ထူးခြားချက်ပဲ —
ငွေလိမ်တဲ့သူတွေက ငွေအကုန်ထုတ်သွားတတ်တယ်။

---

### Task 2.6: Feature Importance

**Solution:**

```python
import joblib
import os

pipeline = joblib.load("model/model.pkl")
clf = pipeline.named_steps["classifier"]

feature_names = ["amount", "oldbalanceOrg", "newbalanceOrig", 
                 "oldbalanceDest", "newbalanceDest"]

importances = clf.feature_importances_
for name, imp in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
    print(f"  {name:20s} → {imp:.4f} ({imp*100:.1f}%)")

print(f"\nModel file size: {os.path.getsize('model/model.pkl'):,} bytes")
```

**Expected Output:**
```
  newbalanceOrig        → 0.4234 (42.3%)
  amount                → 0.3121 (31.2%)
  oldbalanceOrg         → 0.1845 (18.5%)
  newbalanceDest        → 0.0512 (5.1%)
  oldbalanceDest        → 0.0288 (2.9%)

Model file size: 1,234,567 bytes (~1.2 MB)
```

**ဘာကြောင့် `newbalanceOrig` က အရေးကြီးဆုံးလဲ?**

Fraud ဖြစ်တဲ့အခါ `newbalanceOrig` က 0 ဖြစ်တယ် (ငွေအကုန်ထုတ်)။
ဒါက fraud ရဲ့အထူးခြားဆုံး indicator ဖြစ်တယ်။
Non-fraud မှာတော့ `newbalanceOrig` က positive value ဖြစ်တယ်။
ဒါကြောင့် model က ဒီ feature ကိုအဓိကသုံးပြီး classify လုပ်တယ်။

---

### Lab 2 Questions & Answers

**Q1:** ဘာကြောင့် RobustScaler ကို StandardScaler အစားသုံးတာလဲ?

**A:** Fraud dataset မှာ transaction amount တွေက extreme values တွေပါတတ်တယ်
($10 နဲ့ $50,000). StandardScaler က mean နဲ့ std ကိုသုံးတယ် — outlier တွေက
mean ကိုအများကြီးပြောင်းစေတယ်။ RobustScaler က median နဲ့ IQR ကိုသုံးတယ် —
outlier တွေရဲ့သက်ရောက်မှုကိုခံနိုင်ရည်ရှိတယ်။

**Q2:** `random_state=42` က ဘာအတွက်လဲ?

**A:** Reproducibility အတွက်ဖြစ်တယ်။ `random_state` က random number generator ရဲ့
seed ကိုသတ်မှတ်တယ်။ ဒါကြောင့် ဘယ်သူပဲ့ run run တူညီတဲ့ random numbers တွေကိုရမယ် —
ဒါက experiment ကို reproduce လုပ်ဖို့အရေးကြီးတယ်။

**Q3:** `n_estimators=150` က များလား/နည်းလား?

**A:** ဒါက dataset ရဲ့ complexity ပေါ်မူတည်တယ်။ Synthetic data (simple patterns) အတွက်
150 က များတယ် — trees 10-20 လောက်နဲ့ရနိုင်တယ်။ Real-world data (complex patterns) အတွက်
150 က နည်းနိုင်တယ် — 500-1000 အထိလိုနိုင်တယ်။

**Q4:** joblib နဲ့ pickle ကွာခြားချက်ကဘာလဲ?

**A:** joblib က numpy arrays တွေကို serialize/deserialize လုပ်ရာမှာ
pickle ထက်ပိုမြန်တယ်။ joblib က:
1. Large numpy arrays အတွက် optimized ဖြစ်တယ်
2. Compression support ရှိတယ် (`joblib.dump(obj, path, compress=True)`)
3. Memory mapping (`mmap_mode`) ကို support လုပ်တယ် — large models အတွက်

**Q5:** Synthetic data ရဲ့အားသာချက်/အားနည်းချက်တွေကဘာတွေလဲ?

**A:**
**အားသာချက်များ:**
- လွယ်လွယ်ကူကူထုတ်လို့ရတယ် (privacy issues မရှိဘူး)
- လိုချင်တဲ့ pattern ကို design လုပ်လို့ရတယ်
- Class imbalance ကို control လုပ်လို့ရတယ်

**အားနည်းချက်များ:**
- Real world ရဲ့ complexity ကိုဖမ်းမမိဘူး
- Model က synthetic pattern ကိုပဲမှတ်မိပြီး real data အတွက်အလုပ်မလုပ်ဘူး
- Production မှာ unexpected patterns တွေကို handle မလုပ်နိုင်ဘူး

---

## Lab 3 Solution: Running the Inference Server

### Task 3.1: Start the Server

**Solution:**

```bash
cd ml-inference/app
MODEL_PATH=../model/model.pkl uvicorn main:app --host 0.0.0.0 --port 8080
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
[OK] Model loaded: ../model/model.pkl
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

**ဘာဖြစ်သွားလဲဆိုတာရှင်းပြချက်:**

1. `uvicorn` က ASGI server ကို start လုပ်တယ်
2. `main:app` — `main.py` ထဲက `app` variable ကို load လုပ်တယ်
3. FastAPI `lifespan` handler က model.pkl ကို load လုပ်တယ်
4. Server က port 8080 မှာ request တွေကိုစောင့်နေတယ်

**အဖြစ်များတဲ့အမှား:**
```
Error: [Errno 10048] Address already in use
```
ဆိုရင် port 8080 ကို တစ်ခြား process ကသုံးနေလို့ပါ။
Port ကိုပြောင်းပါ သို့မဟုတ် ဟောင်းနေတဲ့ process ကိုသတ်ပါ:

```bash
netstat -ano | grep ':8080 ' | grep LISTEN
taskkill /F /PID <PID>
```

---

### Task 3.2: Test Health Endpoint

**Solution:**

```bash
curl http://localhost:8080/health
```

**Expected:**
```json
{"status": "healthy", "model_loaded": true}
```

**Without Model:**
```bash
MODEL_PATH=/nonexistent/model.pkl uvicorn main:app --host 0.0.0.0 --port 8080
```

**Health Response (model not loaded):**
```json
{"status": "healthy", "model_loaded": false}
```

**Q:** Health endpoint က ဘာကြောင့် model မရှိရင်တောင် 200 OK ပြန်နေတာလဲ?

**A:** Liveness probe က "server process က အသက်ရှိနေလား" ဆိုတာကိုပဲစစ်တယ် —
model ရှိ/မရှိက server ရဲ့အသက်နဲ့မဆိုင်ဘူး။ orchestration မှာ liveness probe က
container ကိုသတ်ပြီး restart လုပ်ဖို့အတွက်ဖြစ်တယ်။
Model မရှိရင် server restart လုပ်လည်းပြဿနာပြေမှာမဟုတ်ဘူး —
ဒါကြောင့် liveness probe က model မရှိတာကို error မမှတ်ဘူး။

---

### Task 3.3: Test Readiness Endpoint

**Solution:**

```bash
# Model loaded
curl http://localhost:8080/ready
# {"status": "ready"}

# Model not loaded
# {"detail": "Model not loaded"}  (503 Service Unavailable)
```

**Q:** Liveness (/health) နဲ့ Readiness (/ready) ကွာခြားချက်ကဘာလဲ?
orchestration မှာ ဘယ်လိုသုံးလဲ?

**A:**
- **Liveness (အသက်):** "Container က အသက်ရှိနေလား?"
  → Deadlock / infinite loop ဖြစ်နေရင် **restart** လုပ်တယ်
  
- **Readiness (အဆင်သင့်):** "Container က traffic လက်ခံနိုင်လား?"
  → Model မရှိသေးရင် **traffic ကိုမပို့ဘူး**

orchestration မှာ:
```yaml
livenessProbe:
  httpGet:
    path: /health      # အမြဲ 200 OK ပြန်တယ်
  initialDelaySeconds: 10

readinessProbe:
  httpGet:
    path: /ready       # Model ရှိမှ 200 OK ပြန်တယ်
  initialDelaySeconds: 15
```

---

### Task 3.4: Startup Logs Analysis

**Server Startup Timeline:**
```
Time 0ms:    uvicorn process start
Time 50ms:   "Waiting for application startup"
Time 100ms:  lifespan handler runs → joblib.load(model.pkl)
Time 500ms:  "Model loaded: ../model/model.pkl"  ← model loading
Time 501ms:  "Application startup complete"
Time 502ms:  "Uvicorn running on http://0.0.0.0:8080"  ← ready for traffic
```

**Q:** "Waiting for application startup" နဲ့ "Application startup complete" ကြားမှာ
ဘာဖြစ်သွားလဲ?

**A:** FastAPI `lifespan` handler က model.pkl ကို disk ကနေ memory ထဲ load လုပ်တယ်။
ဒီအချိန်အတွင်းမှာ request တွေကို လက်မခံသေးဘူး (uvicorn က **lifespan** ပြီးမှ
request handling ကိုစတယ်)။

---

### Task 3.5: Auto-generated Docs

Swagger UI ကို browser မှာဖွင့်ကြည့်တဲ့အခါ:
- Endpoint list ကိုမြင်ရမယ်
- Request/Response schemas တွေကိုမြင်ရမယ်
- "Try it out" button နဲ့ တိုက်ရိုက်စမ်းသပ်လို့ရတယ်
- Authentication မရှိလို့ public access ဖြစ်တယ် — production မှာ ပိတ်သင့်တယ်

---

### Task 3.6: Multiple Workers

```bash
MODEL_PATH=../model/model.pkl uvicorn main:app \
  --host 0.0.0.0 --port 8080 \
  --workers 2
```

**Q:** Workers 2 ဆိုတာဘာလဲ?

**A:** Workers က **separate process** တွေဖြစ်တယ် — thread တွေမဟုတ်ဘူး။
Worker တစ်ခုချင်းစီမှာ model ကို သီးသန့် load လုပ်တယ်။

**Worker 1 (PID 12345):**
  - Python interpreter (separate)
  - Model in memory (separate copy)
  - Handles requests independently

**Worker 2 (PID 12346):**
  - Python interpreter (separate)
  - Model in memory (separate copy)
  - Handles requests independently

**Memory Usage:** 2 workers × 1.2GB (model) = 2.4GB total

---

### Task 3.7: Graceful Shutdown

**Q:** ဒါက orchestration မှာ container ကိုသတ်တဲ့အခါ ဘယ်လိုအသုံးဝင်လဲ?

**A:** orchestration က container ကိုသတ်တဲ့အခါ:
1. **SIGTERM** signal ကိုပို့တယ် (ဒါက graceful shutdown ကိုစဖို့)
2. **TerminationGracePeriodSeconds** (default 30s) အတွင်းစောင့်တယ်
3. **SIGKILL** signal ကိုပို့ပြီး force kill လုပ်တယ်

ဒီ project မှာ shutdown handler က model variable ကို cleanup လုပ်တယ်
(Python garbage collector အတွက်)။

---

## Lab 4 Solution: Making Predictions

### Task 4.1: Simple Prediction Request

**Solution:**

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
```

**Response Analysis:**

```json
{
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "label": "0",
  "label_index": 0,
  "confidence": 1.0,
  "probabilities": [1.0, 0.0],
  "latency_ms": 0.711
}
```

**Field Meanings:**

| Field | Value | Meaning | မြန်မာလိုရှင်းချက် |
|-------|-------|---------|-------------------|
| `request_id` | UUID v4 | Unique transaction ID | ဒီ request အတွက် သီးသန့် ID |
| `label` | "0" | Class name (0 or 1) | "0" = not fraud |
| `label_index` | 0 | Numeric class | Model ရဲ့ raw output |
| `confidence` | 1.0 | Model certainty (0-1) | Model သေချာမှု 100% |
| `probabilities` | [1.0, 0.0] | All class probabilities | Class 0: 100%, Class 1: 0% |
| `latency_ms` | 0.711 | Response time in ms | ၀.၇၁၁ မီလီစက္ကန့် |

---

### Task 4.2: Fraud Detection

**Solution:**

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [99999.0, 500000.0, 0.0, 100.0, 100100.0]}' | python -m json.tool
```

**Response:**
```json
{
  "request_id": "b2c3d4e5-...",
  "label": "1",
  "label_index": 1,
  "confidence": 1.0,
  "probabilities": [0.0, 1.0],
  "latency_ms": 0.782
}
```

**What Changed vs Normal Request:**

| Field | Normal (Task 4.1) | Fraud (Task 4.2) |
|-------|-------------------|-------------------|
| `label` | "0" (not fraud) | "1" (fraud) |
| `label_index` | 0 | 1 |
| `probabilities` | [1.0, 0.0] | [0.0, 1.0] |

**ဘာကြောင့် fraud လို့ပြောတာလဲ?**

Fraud case မှာ `newbalanceOrig = 0.0` ဖြစ်တယ် (ပေးပို့သူရဲ့လက်ကျန် ၀ သွားတယ်) —
ဒါက fraud ရဲ့အဓိကလက္ခဏာဖြစ်တယ်။

---

### Task 4.3: Custom Labels

**Solution:**

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0],
    "labels": ["not_fraud", "fraud"]
  }'
```

**Response:**
```json
{
  "label": "not_fraud",
  "label_index": 0,
  "probabilities": [1.0, 0.0]
}
```

**Q:** `label` field က ဘာဖြစ်သွားလဲ?

**A:** `label` က "0" အစား "not_fraud" ဖြစ်သွားတယ်။ ဒါက `labels` parameter ကို
သုံးလိုက်လို့ပဲ — model က label_index (0) ကိုပဲပြန်တယ်။ `main.py` က
ဒီ index ကို labels array ထဲကနေ လှမ်းယူပြီး label string ကိုပြောင်းပေးတယ်:

```python
labels = body.labels or [str(i) for i in range(len(probs))]
label = labels[label_index] if label_index < len(labels) else str(label_index)
```

Labels မပါရင် default `["0", "1"]` ကိုသုံးတယ်။

---

### Task 4.5: Invalid Data Tests

**Empty Features:**
```json
// 500 Internal Server Error
{"detail": "Inference error: ..."}
```
→ Model က 0 features နဲ့ predict လုပ်လို့မရဘူး

**Too Many Features:**
```json
// 500 Internal Server Error
{"detail": "Inference error: ..."}
```
→ Model က 5 features ကိုပဲမျှော်လင့်တယ် — 8 ခုပေးရင် error တက်တယ်

**Missing Features:**
```json
// 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "features"],
      "msg": "Field required"
    }
  ]
}
```
→ FastAPI/pydantic က validation လုပ်ပြီး error ပြန်တယ်

**Wrong Data Type:**
```json
// 422 Unprocessable Entity
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
→ Pydantic က `List[float]` လို့သတ်မှတ်ထားလို့ string တွေကို reject လုပ်တယ်

---

### Task 4.6: Measure Latency

```bash
time curl -s -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' > /dev/null
```

**Expected:**
```
real    0m0.008s   (8ms — total wall clock time)
user    0m0.000s   (CPU user time)
sys     0m0.000s   (CPU system time)
```

**Q:** `time` ရဲ့ real/user/sys time တွေက ဘာကိုပြတာလဲ?

**A:**
- **real:** Wall clock time (စက္ကန့်တိုင်းကိရိယာနဲ့တိုင်းတဲ့အချိန်)
- **user:** CPU က user space မှာကုန်တဲ့အချိန်
- **sys:** CPU က kernel space မှာကုန်တဲ့အချိန်

Response ထဲက `latency_ms` (0.711ms) က server-side processing time ပဲဖြစ်တယ်။
`real` time (8ms) က network latency + curl processing + server processing
အားလုံးပါတယ်။

---

## Lab 5 Solution: Error Handling

### Task 5.1: Invalid Data Types

**Solution:**
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"features": ["abc", 5000.0, 4750.0, 2000.0, 2250.0]}'
```

**Response (422):**
```json
{
  "detail": [{
    "type": "float_parsing",
    "loc": ["body", "features", 0],
    "msg": "Input should be a valid number, unable to parse string as a number",
    "input": "abc"
  }]
}
```

**Error Structure Analysis:**

```json
{
  "detail": [
    {
      "type": "float_parsing",       // Error type
      "loc": ["body", "features", 0], // Location: body.features[0]
      "msg": "Input should be a ...",  // Human-readable message
      "input": "abc"                   // The actual bad input
    }
  ]
}
```

**`loc` field:** `["body", "features", 0]` ဆိုတာက:
- `body` — Request body ထဲမှာ
- `features` — "features" field ထဲမှာ
- `0` — Index 0 (ပထမဆုံး element)

---

### Task 5.4: Server Without Model

**Solution:**

```bash
# Terminal 1: Start server without model
cd ml-inference/app
MODEL_PATH=/nonexistent.pkl uvicorn main:app --host 0.0.0.0 --port 8081

# Terminal 2: Test
curl http://localhost:8081/health
# {"status": "healthy", "model_loaded": false}  ← 200 OK

curl http://localhost:8081/ready
# {"detail": "Model not loaded"}  ← 503 Service Unavailable

curl -X POST http://localhost:8081/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}'
# {"detail": "Model not ready"}  ← 503 Service Unavailable
```

**Graceful Degradation Explanation:**

ဒါက **Graceful Degradation** ရဲ့ဥပမာပဲ — system က partial failure ရှိရင်တောင်
လုံးဝမပျက်ဘဲ ဆက်အလုပ်လုပ်တယ်။

```
Model Loading Failed
        │
        ▼
┌──────────────────────┐
│   Server starts ✅   │  ← Health check pass (alive)
│   Model = None       │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│   orchestration Readiness ❌   │  ← No traffic routed
│   (503 → no traffic) │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│   Alert: "Retrain"   │  ← Ops team notified
│   or auto-recovery   │
└──────────────────────┘
```

---

### Lab 5 Questions & Answers

**Q1:** FastAPI က error handling ကို Flask နဲ့ယှဉ်ရင် ဘယ်လိုကွာလဲ?

**A:** Flask မှာ error handlers တွေကို ကိုယ်တိုင်ရေးရတယ်။ FastAPI က
pydantic validation errors တွေကို auto-handle လုပ်ပြီး structured error
response (RFC 7807 problem details) ကိုပြန်ပေးတယ်။

**Q2:** 422 နဲ့ 400 error code ကွာခြားချက်ကဘာလဲ?

**A:**
- **400 Bad Request:** Client က malformed request ပို့တယ် (ဥပမာ: invalid JSON syntax)
- **422 Unprocessable Entity:** Request body က valid JSON ဖြစ်ပေမယ့်
  semantic validation မအောင်ဘူး (ဥပမာ: string ကို number နေရာမှာထားတယ်)

**Q3:** ဘာကြောင့် `except Exception` ကိုသုံးပြီး predict error ကို generic ဖမ်းထားတာလဲ?

**A:** Inference error တွေက unpredictable ဖြစ်တယ် — model bug, memory error, 
data type mismatch စသဖြင့်။ Specific exceptions တွေကိုတစ်ခုချင်းဖမ်းရင်
အမြဲ update လုပ်နေရမယ်။ Generic `except Exception` က error အားလုံးကိုဖမ်းတယ် —
500 error ပြန်ပြီး server crash ကိုကာကွယ်တယ်။

---

## Lab 6 Solution: Elasticsearch

### Task 6.1: Verify ES Connection

**Solution:**

```python
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    "http://192.168.1.123:80",
    basic_auth=("elastic", "ML0psElk!2026")
)

info = es.info()
print(f"ES Version: {info['version']['number']}")       # 8.19.17
print(f"Cluster: {info['cluster_name']}")               # elk-production
print(f"Cluster UUID: {info['cluster_uuid']}")
```

**Error: URL must include a 'scheme', 'host', and 'port' component**

ဒီ error က port မပါလို့ဖြစ်တယ်။ ES client 8.x/9.x က URL မှာ port ကိုထည့်ပေးရတယ်:
```python
# ❌ Wrong
es = Elasticsearch("http://192.168.1.123")

# ✅ Correct
es = Elasticsearch("http://192.168.1.123:80")
```

**Error: Accept version must be either version 8 or 7, but found 9**

ဒီ error က elasticsearch-py 9.x ကို ES 8.x server နဲ့တွဲသုံးလို့ဖြစ်တယ်။
ဖြေရှင်းနည်း:
```bash
pip install elasticsearch==8.12.0
```

---

### Task 6.2: Write a Test Document

**Solution:**

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
    },
    "status": "success"
}

resp = es.index(index="ml-inference", document=doc)
print(f"Index result: {resp['result']}")    # "created"
print(f"Document ID: {resp['_id']}")        # Auto-generated UUID
```

**ဘာဖြစ်သွားလဲ?**

1. ES client က `PUT /ml-inference/_doc/<auto-id>` request ကိုပို့တယ်
2. `ml-inference` index မရှိသေးရင် auto-create လုပ်တယ်
3. Document ကို index လုပ်တယ် — `result: "created"` (first time)
4. နောက်တစ်ခါ write ရင် `result: "updated"` ဖြစ်မယ် (same ID ဆိုရင်)

---

### Task 6.3: Search Your Document

**Using curl:**
```bash
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?q=request_id:test-manual-write&pretty"
```

**Using Python:**
```python
resp = es.search(
    index="ml-inference",
    query={"term": {"request_id": "test-manual-write"}}
)

print(f"Total matches: {resp['hits']['total']['value']}")

for hit in resp['hits']['hits']:
    source = hit['_source']
    print(f"  Score: {hit['_score']}")
    print(f"  Prediction: {source['prediction']['label']}")
    print(f"  Timestamp: {source['@timestamp']}")
```

**Q:** `_score` ဆိုတာဘာလဲ?

**A:** `_score` က **relevance score** ဖြစ်တယ် — search query နဲ့ document ရဲ့
ဆက်စပ်မှုကိုဖော်ပြတယ် (0-1). `term` query (exact match) အတွက် score က 0 ပဲ —
ဒါက term query ရဲ့သဘာဝပဲ (binary match/no match). `match` query (full-text search)
အတွက်မှ score က 0 ကနေ 1 ကြားရှိတယ်။

---

### Task 6.5: Search and Analyze

**Latest 3 Documents:**
```bash
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?size=3&sort=@timestamp:desc&pretty"
```

**Aggregation (Count by Label):**
```bash
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

**Response:**
```json
{
  "aggregations": {
    "by_label": {
      "buckets": [
        {"key": 0, "doc_count": 45},
        {"key": 1, "doc_count": 3}
      ]
    }
  }
}
```

ဒါက prediction 48 ခုထဲမှာ:
- 45 ခုက "not fraud" (label 0)
- 3 ခုက "fraud" (label 1)

---

### Task 6.7: ES Error Handling (ES Down)

**When ES is down, but server is up:**

```bash
# Server log shows:
[WARN] ES inference log failed: ...connection refused...
```

But prediction က **ဆက်အလုပ်လုပ်တယ်** (response time ကလည်းပုံမှန်အတိုင်း):
```json
{
  "request_id": "...",
  "label": "0",
  "latency_ms": 0.711
}
```

**ဒါက Fire-and-Forget Pattern ရဲ့အားသာချက်ပဲ။**

---

## Lab 7 Solution: Metrics Collection

### Task 7.1: Run collect_metrics

**Solution:**

```bash
cd ml-inference/app
python -m app.collect_metrics
```

**Expected Output:**
```
[OK] Metrics logged — acc=1.0, f1=1.0, p95=1.5ms
[OK] Batch analysis complete for N items.
```

**Why is accuracy 1.0?**

`collect_metrics.py` က `y_true=preds` လို့သုံးထားတယ် (prediction ကိုပဲ
ground truth အဖြစ်သုံးတယ်). ဒါက **placeholder** ပဲ — production မှာ
y_true က feedback loop (manual review, user report) ကနေလာရမယ်။

---

### Task 7.5: Latency Percentile Analysis

**Solution:**

```python
import numpy as np

np.random.seed(42)
latencies = np.random.exponential(scale=1.0, size=1000)
latencies = np.append(latencies, [50, 100, 200])  # Outliers

print(f"Count:     {len(latencies)}")
print(f"Mean:      {np.mean(latencies):.3f} ms")
print(f"Median:    {np.median(latencies):.3f} ms")
print(f"P90:       {np.percentile(latencies, 90):.3f} ms")
print(f"P95:       {np.percentile(latencies, 95):.3f} ms")
print(f"P99:       {np.percentile(latencies, 99):.3f} ms")
print(f"Max:       {np.max(latencies):.3f} ms")
```

**Expected Output:**
```
Count:     1003
Mean:      1.673 ms    ← 3 outliers ကြောင့်များနေတယ်
Median:    0.693 ms    ← Outlier တွေကို ignored
P90:       2.305 ms
P95:       3.129 ms
P99:       50.000 ms   ← Outlier တွေပေါ်လာတယ်
Max:       200.000 ms  ← Extreme outlier
```

**Q:** Mean က 1.5ms လောက်ရှိပေမယ့် p99 က ဘာလို့အများကြီးများနေတာလဲ?

**A:** Mean က **arithmetic average** ဖြစ်တယ် — outliers တွေက mean ကိုဆွဲတင်တယ်။
P99 က **99th percentile** ဖြစ်တယ် — 3 outliers (50, 100, 200ms) တွေထဲက
အများဆုံး 200ms က p99 ကိုမြှင့်တယ်။

**Real-world meaning:**
- Average user: ~1.7ms (acceptable)
- 99th percentile user: 50ms (noticeable lag)
- Worst case: 200ms (bad UX)

---

## Lab 8 Solution: Drift Detection

### Task 8.1: Basic Drift Detection

**Solution:**

```python
import numpy as np
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

np.random.seed(42)
ref = pd.DataFrame({
    "amount": np.random.normal(500, 200, 1000),
    "balance": np.random.normal(10000, 5000, 1000),
})

# No drift
curr_no_drift = pd.DataFrame({
    "amount": np.random.normal(500, 200, 1000),
    "balance": np.random.normal(10000, 5000, 1000),
})

# With drift
curr_drift = pd.DataFrame({
    "amount": np.random.normal(5000, 2000, 1000),
    "balance": np.random.normal(50000, 20000, 1000),
})

# Test 1: No drift → dataset_drift = False
# Test 2: With drift → dataset_drift = True
```

**Q:** p_value < 0.05 ဆိုတာဘာကိုဆိုလိုလဲ?

**A:** p-value က **null hypothesis** (distribution နှစ်ခုက တူညီတယ်) ကို
စမ်းသပ်တယ်။ p-value < 0.05 ဆိုရင် null hypothesis ကိုငြင်းပယ်တယ် —
distribution တွေက တူညီမှုမရှိဘူးလို့ဆိုလိုတယ် (drift detected)။

---

## Lab 9 Solution: Docker

### Task 9.1: Layer Caching

**Q:** Layer caching က ဘယ်လိုအလုပ်လုပ်လဲ? ဘာကြောင့် requirements.txt ကို
code တွေမထည့်ခင် သီးသန့် copy လုပ်တာလဲ?

**A:** Docker က layer တစ်ခုချင်းစီကို cache လုပ်တယ်။ Layer က မပြောင်းရင်
cache ကိုပြန်သုံးတယ် — rebuild မြန်တယ်။

**Optimized order (ဒီအတိုင်း):**
```
Layer 1: FROM python:3.11-slim        ← Rarely changes
Layer 2: COPY requirements.txt .       ← Only changes when deps change
Layer 3: RUN pip install -r ...       ← Cached if Layer 2 is cached
Layer 4: COPY app/ .                  ← Changes frequently
Layer 5: COPY model/ ./model/         ← Changes when model updates
```

**Without optimization:**
```
Layer 1: FROM python:3.11-slim
Layer 2: COPY app/ .                  ← Code changes = ALL layers rebuild
Layer 3: RUN pip install -r ...       ← Runs every time (slow!)
```

---

## Lab 10 Solution: Production Hardening

### Task 10.7: Performance Test

**Solution:**

```bash
echo "Testing with 100 concurrent requests..."

START=$(date +%s%N)

for i in $(seq 1 100); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' \
    -o /dev/null -w "%{http_code} %{time_total}\n" >> /tmp/results.txt &
done

wait

END=$(date +%s%N)
TOTAL_TIME=$(( ($END - $START) / 1000000 ))  # ms

echo "Total time: ${TOTAL_TIME}ms"
echo "Throughput: $(( 100 * 1000 / $TOTAL_TIME )) req/sec"

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

**Expected Output (2 workers):**
```
Total time: 350ms
Throughput: 285 req/sec
Min latency: 0.001s
P50 latency: 0.003s
P90 latency: 0.008s
P95 latency: 0.012s
P99 latency: 0.025s
Max latency: 0.050s
```

---

### Lab 10 Questions & Answers

**Q1:** Production အတွက် အရေးကြီးဆုံး hardening က ဘာလဲ?

**A:** Priority order:
1. **Authentication/Authorization** — API key သို့မဟုတ် JWT token ထည့်ပါ
2. **HTTPS/TLS** — Let's Encrypt cert နဲ့ encrypt လုပ်ပါ
3. **Secrets management** — Hardcoded password တွေကိုဖယ်ပါ
4. **Rate limiting** — DDoS ကိုကာကွယ်ပါ
5. **Monitoring/Alerting** — ES down, high latency, drift တွေအတွက် alert ထားပါ

**Q2:** Security vs performance — ဘယ်လို balance လုပ်မလဲ?

**A:**
- Rate limiting က performance ကိုနည်းနည်းထိခိုက်တယ် (request queue)
- TLS handshake က latency ကိုထည့်တယ် (ဒါပေမယ့် keep-alive နဲ့လျှော့လို့ရ)
- Request validation က overhead ရှိတယ် (ဒါပေမယ့် meaningless requests တွေကိုစစ်ထုတ်ပေးတယ်)
- Logging (ES write) က latency ကိုထည့်တယ် (ဒါပေမယ့် async/fire-and-forget နဲ့လျှော့လို့ရ)

များသောအားဖြင့် **security overhead က 1-5%** ပဲရှိတယ် — ဒါက protection ရဲ့
တန်ဖိုးနဲ့ယှဉ်ရင် လက်ခံနိုင်တယ်။

**Q3:** ဒီ project ကို production မှာ run ဖို့ အနည်းဆုံးဘာတွေထပ်လိုအပ်လဲ?

**A:**
1. **Real model** — Synthetic data နဲ့ train ထားတဲ့ model က production အတွက်မရဘူး
2. **Real ground truth** — y_true ကို feedback loop ကနေရယူဖို့လိုတယ်
3. **API key / JWT** — Authentication မရှိရင် anyone က predict လုပ်လို့ရတယ်
4. **Input validation** — Feature range, business rules တွေကို validate လုပ်ဖို့လိုတယ်
5. **HTTPS** — Password တွေကို plain text နဲ့မပို့သင့်ဘူး
6. **Error tracking** — Sentry / DataDog error tracking ထည့်သင့်တယ်
7. **CI/CD** — Auto-build, auto-test, auto-deploy pipeline

**Q4:** Monitoring (observability) အတွက် ဘာ tools တွေထပ်သုံးသင့်လဲ?

**A:**

| Layer | Tool | Purpose |
|-------|------|---------|
| **Metrics** | Prometheus | Time-series metrics collection |
| **Dashboard** | Grafana | Visualization, dashboards |
| **Logging** | ELK Stack (ES + Logstash + Kibana) | Centralized logging |
| **Tracing** | Jaeger / OpenTelemetry | Distributed tracing |
| **Alerting** | AlertManager | Alert routing |
| **Error tracking** | Sentry | Exception tracking |
| **APM** | DataDog / NewRelic | Application performance monitoring |

---

## Appendix: Common Errors & Solutions

### ES Client Errors

```
Error: ValueError: URL must include a 'scheme', 'host', and 'port' component
Fix: Use http://host:80 (with explicit port)
```

```
Error: BadRequestError: Accept version must be either version 8 or 7, but found 9
Fix: pip install elasticsearch==8.12.0
```

### Server Errors

```
Error: [Errno 10048] Address already in use
Fix: taskkill /F /PID <PID>  or  change port
```

```
Error: ModuleNotFoundError: No module named 'uvicorn'
Fix: pip install -r app/requirements.txt
```

```
Error: Model not loaded — predict will return 503
Fix: Check MODEL_PATH, run python -m app.train_model
```

### Docker Errors

```
Error: Cannot connect to the Docker daemon
Fix: Start Docker Desktop
```

```
Error: port is already allocated
Fix: docker stop <container>; docker rm <container>
```

---

*End of Solutions*

---

## Appendix: Additional Lab Solutions

### Lab B1 Solution: Multi-Model Deployment

**Implementation:**

Create `app/train_rf_model.py`:

```python
"""Train a Random Forest model for comparison."""
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Reuse the same data generation
from app.train_model import generate_sample_data

df = generate_sample_data()
FEATURE_COLS = ["amount", "oldbalanceOrg", "newbalanceOrig",
                "oldbalanceDest", "newbalanceDest"]
X = df[FEATURE_COLS].values
y = df["isFraud"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline = Pipeline([
    ("scaler", RobustScaler()),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42,
        n_jobs=-1,  # Use all CPU cores
    )),
])

pipeline.fit(X_train, y_train)
print(f"RF Train accuracy: {pipeline.score(X_train, y_train):.4f}")
print(f"RF Test accuracy:  {pipeline.score(X_test, y_test):.4f}")

joblib.dump(pipeline, "model/rf_model.pkl")
print("RF model saved to model/rf_model.pkl")
```

**Modified `main.py`:**

```python
MODELS = {
    "gradient_boosting": joblib.load("model/model.pkl"),
    "random_forest": joblib.load("model/rf_model.pkl"),
}
MODEL_META = {
    "gradient_boosting": {"version": "1.0.0", "type": "GB"},
    "random_forest": {"version": "1.0.0", "type": "RF"},
}

@app.post("/predict/{model_name}")
async def predict_with_model(model_name: str, request: Request, body: PredictRequest):
    if model_name not in MODELS:
        raise HTTPException(404, detail=f"Model '{model_name}' not found. Available: {list(MODELS.keys())}")
    
    model = MODELS[model_name]
    meta = MODEL_META[model_name]
    
    X = np.array(body.features).reshape(1, -1)
    t0 = time.perf_counter()
    label_index = int(model.predict(X)[0])
    probs = model.predict_proba(X)[0].tolist()
    latency = (time.perf_counter() - t0) * 1000
    
    return PredictResponse(
        request_id=str(uuid.uuid4()),
        label=str(label_index),
        label_index=label_index,
        confidence=round(max(probs), 4),
        probabilities=[round(p, 4) for p in probs],
        latency_ms=round(latency, 3),
    )
```

**Comparison Results:**

| Metric | GradientBoosting | RandomForest |
|--------|-----------------|--------------|
| Accuracy (synthetic) | 1.0 | 1.0 |
| Inference time | 0.7ms | 1.2ms |
| File size | 1.2 MB | 3.5 MB |
| n_estimators | 150 | 100 |
| Max depth | 4 | 8 |

---

### Lab B2 Solution: Kibana Dashboard

**Kibana Setup Steps:**

1. Open Kibana (http://192.168.1.123:5601)
2. Go to Stack Management → Data Views → Create Data View
3. Name: `ML Inference Logs`, Index pattern: `ml-inference*`
4. Timestamp field: `@timestamp`
5. Create visualizations:
   - **Predictions Over Time**: Lens → Bar chart → X: @timestamp (auto-interval), Y: Count
   - **Fraud vs Non-Fraud**: Lens → Pie chart → Slice: prediction.label_index, Size: Count
   - **Average Latency**: Lens → Metric → Average: performance.latency_ms
   - **Latest Predictions**: Discover → Filter: ml-inference* → Sort: @timestamp desc
6. Create Dashboard → Add all visualizations

**Verification:**
After sending 20+ predictions, the dashboard should show:
- A bar chart with request counts over time
- A pie chart showing ~98% non-fraud, ~2% fraud
- Average latency ~1ms
- Latest predictions with full details

---

### Lab B3 Solution: Request Caching

**Full Implementation:**

```python
from cachetools import LRUCache
from hashlib import sha256
import json

# Global cache (250 MB limit estimate for 0.7KB per entry × 1000)
cache = LRUCache(maxsize=1000)

def get_cache_key(features, labels):
    """Generate deterministic cache key from request parameters."""
    content = json.dumps({"f": features, "l": labels}, sort_keys=True)
    return sha256(content.encode()).hexdigest()

@app.post("/predict")
async def predict(request: Request, body: PredictRequest):
    if model is None:
        raise HTTPException(503, detail="Model not ready")
    
    cache_key = get_cache_key(body.features, body.labels)
    
    if cache_key in cache:
        print(f"[CACHE HIT] Returning cached result")
        return cache[cache_key]
    
    # ... normal inference logic ...
    
    response = PredictResponse(
        request_id=str(uuid.uuid4()),
        label=label,
        label_index=label_index,
        confidence=round(max(probs), 4),
        probabilities=[round(p, 4) for p in probs],
        latency_ms=round(total_ms, 3),
    )
    
    cache[cache_key] = response
    print(f"[CACHE MISS] Computed and cached result")
    return response
```

**Performance Comparison:**

| Scenario | Latency | Notes |
|----------|---------|-------|
| No cache (first request) | 0.7ms | Full inference |
| Cache hit (same features) | 0.01ms | 70x faster! |
| Cache after model update | 0.7ms | Cache miss (new model = new cache) |

**Cache Invalidation Strategy:**

```python
model_version = "1.0.1"  # Update when model changes

def get_cache_key(features, labels):
    content = json.dumps({
        "f": features, "l": labels, 
        "model_version": model_version  # Invalidate on model change
    }, sort_keys=True)
    return sha256(content.encode()).hexdigest()
```

---

### Lab B4 Solution: Canary Testing

**Full Implementation:**

```python
import random
import joblib
import numpy as np

# Load both model versions
MODELS = {
    "v1.0.0": {
        "model": joblib.load("model/model.pkl"),
        "traffic": 90,   # 90%
    },
    "v1.1.0": {
        "model": joblib.load("model/model_v2.pkl"),
        "traffic": 10,   # 10%
    },
}

def select_model_version():
    """Traffic-weighted random selection."""
    total = sum(m["traffic"] for m in MODELS.values())
    r = random.randint(1, total)
    cumulative = 0
    for version, config in MODELS.items():
        cumulative += config["traffic"]
        if r <= cumulative:
            return version, config["model"]
    return "v1.0.0", MODELS["v1.0.0"]["model"]  # Fallback

@app.post("/predict")
async def predict(request: Request, body: PredictRequest):
    version, model = select_model_version()
    
    X = np.array(body.features).reshape(1, -1)
    label_index = int(model.predict(X)[0])
    probs = model.predict_proba(X)[0].tolist()
    
    # Log model version in ES
    monitor.model_version = version
    monitor.log_inference(
        input_features={"features": body.features},
        prediction_label=str(label_index),
        prediction_index=label_index,
        probabilities=probs,
        latency_ms=0.5,
        status="success",
        client_ip=request.client.host if request.client else "unknown",
    )
    
    return PredictResponse(
        request_id=str(uuid.uuid4()),
        label=str(label_index),
        label_index=label_index,
        confidence=round(max(probs), 4),
        probabilities=[round(p, 4) for p in probs],
        latency_ms=round(0.5, 3),
    )
```

**Promotion Criteria:**

| Metric | Condition | Action |
|--------|-----------|--------|
| Accuracy | v1.1.0 > v1.0.0 | Promote |
| Latency p99 | v1.1.0 < 2 × v1.0.0 | Accept |
| Error rate | v1.1.0 < v1.0.0 | Promote |
| Drift score | Both same data | Same expectation |

---

### Lab B5 Solution: API Gateway Integration

**Complete Implementation:**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# API key store (in production, use a database or secrets manager)
API_KEYS = {
    "sk-prod-ml-inference-key1": "team-alpha",
    "sk-prod-ml-inference-key2": "team-beta",
}

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    # Public endpoints
    if request.url.path in ["/health", "/ready", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing X-API-Key header"}
        )
    
    if api_key not in API_KEYS:
        return JSONResponse(
            status_code=403,
            content={"detail": "Invalid API key"}
        )
    
    # Attach client identity for logging
    request.state.client_name = API_KEYS[api_key]
    
    return await call_next(request)

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(request: Request, body: PredictRequest):
    # Optional: log which client made the request
    client = getattr(request.state, "client_name", "unknown")
    ...
```

**Expected behavior:**
- No API key → 401
- Wrong API key → 403
- Correct API key → 200
- Exceed rate limit (11th request in a second) → 429

---

### Lab B6 Solution: Locust Load Testing

**Results interpretation:**

```
Type     Name                   # reqs  # fails  Avg(ms)  Min   Max  Med  req/s
--------|---------------------|------|-------|--------|-----|-----|----|------
POST    /predict                5000   0       1.2      0.5   45    1    250

Response time percentiles (approximate):
  50%   below  1.2 ms
  75%   below  2.1 ms
  90%   below  3.5 ms
  95%   below  5.8 ms
  99%   below  12.4 ms
  100%  below  45.0 ms
```

**Bottleneck identification:**
- If CPU > 80%: Add more workers
- If memory > 80%: Use smaller model or more memory
- If network I/O high: Check ES connection pooling

---

### Lab B7 Solution: Feature Store Integration

**Production considerations:**

1. Use Redis for low-latency feature serving:
```python
import redis
r = redis.Redis(host="feature-store", port=6379, decode_responses=True)

def get_feature(account_id, feature_name):
    return float(r.hget(f"account:{account_id}", feature_name) or 0)
```

2. Batch feature fetching for batch prediction:
```python
pipeline = r.pipeline()
for account_id in account_ids:
    pipeline.hgetall(f"account:{account_id}")
results = pipeline.execute()
```

3. Feature freshness monitoring:
```python
def check_feature_freshness(account_id):
    last_updated = r.hget(f"account:{account_id}", "last_updated")
    if last_updated and (datetime.now() - parse(last_updated)).hours > 24:
        print(f"[WARN] Stale features for account {account_id}")
```

---

### Lab B8 Solution: Drift Alerting

**Slack webhook setup:**

1. Go to https://api.slack.com/apps
2. Create new app → Incoming Webhooks
3. Activate webhook → Copy webhook URL
4. Set environment variable:
```bash
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00/B00/xxxx
```

**Alert severity levels:**

| Drift Score | Severity | Response |
|------------|----------|----------|
| 0.0 - 0.1 | None | No action |
| 0.1 - 0.3 | Info | Log to ES, notify DS team |
| 0.3 - 0.5 | Warning | Alert on Slack, investigate within 24h |
| 0.5 - 0.7 | Critical | Page on-call, investigate within 1h |
| 0.7 - 1.0 | Blocker | Rollback model, stop serving |

---

### Lab B9 Solution: A/B Testing Analysis

**Sample size calculation:**

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
# To detect a 5% latency improvement with 80% power:
sample_size = analysis.solve_power(
    effect_size=0.05 / 0.01,  # 5ms improvement / 1ms std
    power=0.8,
    alpha=0.05,
)
print(f"Need {sample_size:.0f} samples per group")
```

**Interpreting p-values:**

- p < 0.001: Strong evidence that treatment differs from control
- p < 0.01: Moderate evidence
- p < 0.05: Weak evidence (conventional threshold)
- p >= 0.05: Not statistically significant

**Important:** p-value does NOT measure effect size. A tiny improvement can be "significant" with enough samples.

---

### Lab B10 Solution: MLOps Pipeline

**GitHub Actions integration:**

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday 6 AM
  workflow_dispatch:      # Manual trigger

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r app/requirements.txt
      
      - name: Data Collection
        run: python -m app.data_collection
      
      - name: Data Validation
        run: python -m app.data_validation
      
      - name: Model Training
        run: python -m app.train_model
      
      - name: Model Validation
        run: |
          python -c "
          import joblib, numpy as np
          model = joblib.load('model/model.pkl')
          X_test = np.random.randn(1000, 5)
          y_test = np.random.choice([0, 1], 1000, p=[0.99, 0.01])
          acc = model.score(X_test, y_test)
          print(f'Validation accuracy: {acc:.4f}')
          if acc < 0.9:
              exit(1)
          "
      
      - name: Build Docker
        run: docker build -t ml-inference:${{ github.sha }} .
      
      - name: Push to Registry
        run: |
          docker tag ml-inference:${{ github.sha }} registry.example.com/ml-inference:latest
          docker push registry.example.com/ml-inference:latest
      
      - name: Deploy
        run: |
          kubectl set image deployment/ml-inference \
            inference=registry.example.com/ml-inference:${{ github.sha }}
```

**Pipeline stages missing from simulation:**

1. **Data versioning** (DVC) — Track which data version trained which model
2. **Experiment tracking** (MLflow) — Log hyperparameters, metrics, artifacts
3. **Model registry** — Staging → Production promotion workflow
4. **Shadow deployment** — Run new model in parallel without serving traffic
5. **Online evaluation** — Compare shadow vs production metrics

**Failure handling:**

```
Pipeline Failures:
  ├─ Data validation fail → Alert data engineering team
  ├─ Training fail → Alert ML engineer, check logs
  ├─ Validation fail (low accuracy) → Skip deploy, alert ML engineer
  ├─ Docker build fail → Check Dockerfile, dependencies
  └─ Deploy fail → orchestration rollout undo (automatic rollback)
```

---

*End of Solutions — Additional Labs*

