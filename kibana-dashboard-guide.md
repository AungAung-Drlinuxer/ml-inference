# Kibana Dashboard Guide — ML Inference Monitoring

**Based on Lab B2 from `lab.md`**

---

## 1. Prerequisites — မလုပ်မီပြင်ဆင်ရန်

### 1.1 Data ရှိဖို့လိုအပ်ချက်

Kibana dashboard ဆောက်ဖို့ `ml-inference` index ထဲမှာ data တွေရှိဖို့လိုတယ်။
အနည်းဆုံး predictions ၂၀-၃၀ လောက်ရှိမှ visualization တွေက အဓိပ္ပါယ်ရှိမယ်။

```bash
# Server ကို ES နဲ့ start လုပ်ပါ
cd ml-inference/app
MODEL_PATH=../model/model.pkl \
ES_HOST=http://192.168.1.123:80 \
ES_USER=elastic \
ES_PASS='ML0psElk!2026' \
uvicorn main:app --host 0.0.0.0 --port 8080

# Predictions ၃၀ လောက်ပို့ပါ (ပုံမှန် + fraud ရောထားပါ)
for i in $(seq 1 25); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [250.0, 5000.0, 4750.0, 2000.0, 2250.0]}' > /dev/null
done

for i in $(seq 1 5); do
  curl -s -X POST http://localhost:8080/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [99999.0, 500000.0, 0.0, 100.0, 100100.0]}' > /dev/null
done
```

### 1.2 Data ရောက်မရောက်စစ်ဆေးခြင်း

```bash
# ES index ထဲမှာ doc တွေရှိလား?
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/_cat/indices/ml-*?v"

# နောက်ဆုံး document ၃ ခု
curl -u elastic:'ML0psElk!2026' \
  "http://192.168.1.123:80/ml-inference/_search?size=3&sort=@timestamp:desc&pretty"
```

---

## 2. Kibana ကိုဖွင့်ခြင်း

### 2.1 Kibana URL

သင့် ES cluster ရဲ့ Kibana URL ကို ဖွင့်ပါ:

```
http://192.168.1.122:5601
```

(ဒါမှမဟုတ် သင့် environment အတိုင်း — Kibana VIP က 192.168.1.122:80 ဆိုရင်
http://192.168.1.122:80 ကိုသုံးပါ)

### 2.2 Login

```
Username: elastic
Password: ML0psElk!2026
```

---

## 3. Data View (Index Pattern) ဆောက်ခြင်း

Kibana မှာ data တွေကိုကြည့်ဖို့ပထမဆုံး **Data View** တစ်ခုဆောက်ရမယ်။

### Step-by-Step:

```
Step 1: Kibana Home Page
        ┌──────────────────────────────────┐
        │  ☰ (Menu) → Stack Management     │
        │  → Data Views                    │
        └──────────────────────────────────┘
        
Step 2: Create Data View
        ┌──────────────────────────────────┐
        │  [Create data view] ကိုနှိပ်ပါ     │
        │                                   │
        │  Name:        ML Inference Logs   │
        │  Index pattern: ml-inference*     │
        │  Timestamp:   @timestamp          │
        │                                   │
        │  [Save data view to Kibana]       │
        └──────────────────────────────────┘
```

**ရှင်းလင်းချက်:**

| Field | Value | ဘာကြောင့်ဒီလိုထားလဲ |
|-------|-------|---------------------|
| Name | `ML Inference Logs` | Dashboard မှာပြမယ့် display name |
| Index pattern | `ml-inference*` | `ml-inference` နဲ့ `ml-inference-000001` (data stream) ကိုပါကျုံ့မယ် |
| Timestamp | `@timestamp` | Time-based filtering အတွက် |

---

## 4. Visualizations ဆောက်ခြင်း

Kibana **Lens** ကို သုံးပြီး visualization တွေဆောက်မယ်။
(သို့မဟုတ် **Visualize Library** ကိုလည်းသုံးလို့ရတယ် — ဒီမှာ Lens နဲ့ပြထားတယ်)

### 4.1 Visualization 1 — Predictions Over Time (Bar Chart)

**Purpose:** Request တွေက အချိန်နဲ့အမျှ ဘယ်လောက်ရှိလဲဆိုတာကြည့်ဖို့

```
Step 1: ☰ → Analytics → Lens
Step 2: Select data view: ML Inference Logs
Step 3: Visualization type → Bar chart (vertical)
Step 4: Configure:

  X-axis (Horizontal):
    ┌─────────────────────────────┐
    │ Drag: @timestamp            │
    │ Aggregation: Date Histogram │
    │ Interval: Auto              │
    └─────────────────────────────┘
    
  Y-axis (Vertical):
    ┌─────────────────────────────┐
    │ Drag: @timestamp            │
    │ Aggregation: Count          │
    │ Label: "Request Count"      │
    └─────────────────────────────┘

Step 5: [Save] → Title: "Predictions Over Time"
```

**Expected Result:**
```
Request Count
    10 │  ██
     8 │  ██  ██
     6 │  ██  ██  ██
     4 │  ██  ██  ██
     2 │  ██  ██  ██  ██
       └────────────────────► Time
         10:00  10:05  10:10
```

**ဘာကိုပြတာလဲ:** ဒီ bar chart က အချိန်ကာလအလိုက် request အရေအတွက်ကိုပြတယ်။
Production မှာ traffic spike တွေ၊ drop တွေကိုသိဖို့အသုံးဝင်တယ်။

---

### 4.2 Visualization 2 — Fraud vs Non-Fraud Distribution (Pie Chart)

**Purpose:** Prediction label တွေရဲ့အချိုးကိုကြည့်ဖို့

```
Step 1: ☰ → Analytics → Lens
Step 2: Visualization type → Pie chart (donut)
Step 3: Configure:

  Slice by:
    ┌──────────────────────────────────┐
    │ Drag: prediction.label_index     │
    │                                  │
    │ Filter လုပ်ရန်:                  │
    │ prediction.label_index: 0 → "Not Fraud"  │
    │ prediction.label_index: 1 → "Fraud"      │
    └──────────────────────────────────┘
    
  Size by:
    ┌──────────────────────────────────┐
    │ Drag: @timestamp                 │
    │ Aggregation: Count               │
    └──────────────────────────────────┘

Step 4: [Save] → Title: "Fraud vs Non-Fraud"
```

**Expected Result:**
```
        ╭─────────╮
       ╱  Fraud   ╲       ← 5 requests (16%)
      │   16%      │
       ╲          ╱
        ╰────────╯
     ╭─────────────────╮
    ╱   Not Fraud       ╲    ← 25 requests (84%)
   │      84%             │
    ╲                   ╱
     ╰─────────────────╯
```

**ဘာကိုပြတာလဲ:** ဒီ pie chart က fraud နဲ့ non-fraud အချိုးကိုပြတယ်။
Production မှာ fraud ratio က ရုတ်တရက်များလာရင် စစ်ဆေးဖို့လိုတယ်။

---

### 4.3 Visualization 3 — Average Latency (Metric)

**Purpose:** Inference latency ရဲ့ average ကိုကြည့်ဖို့

```
Step 1: ☰ → Analytics → Lens
Step 2: Visualization type → Metric
Step 3: Configure:

  Metric value:
    ┌──────────────────────────────────┐
    │ Drag: performance.latency_ms    │
    │ Aggregation: Average            │
    │ Label: "Avg Latency (ms)"       │
    │ Decimals: 3                     │
    └──────────────────────────────────┘

Step 4: Color range:
    ┌──────────────────────────────────┐
    │ Green:   0 - 2ms  (normal)       │
    │ Yellow:  2 - 5ms  (warning)      │
    │ Red:     > 5ms    (critical)     │
    └──────────────────────────────────┘

Step 5: [Save] → Title: "Average Inference Latency"
```

**Expected Result:**
```
┌─────────────────────────┐
│                         │
│      0.711 ms           │
│   Avg Latency (ms)      │
│                         │
│   (အစိမ်းရောင် = normal)  │
└─────────────────────────┘
```

**ဘာကိုပြတာလဲ:** ဒီ metric က average latency ကိုပြတယ်။
Production မှာ latency များလာရင် model ဒါမှမဟုတ် infrastructure မှာ
ပြဿနာရှိတယ်လို့သိနိုင်တယ်။

---

### 4.4 Visualization 4 — Latency Distribution (Heatmap)

**Purpose:** Latency တန်ဖိုးတွေရဲ့ distribution ကိုကြည့်ဖို့ (p95, p99 ကိုခန့်မှန်း)

```
Step 1: ☰ → Analytics → Lens
Step 2: Visualization type → Heatmap
Step 3: Configure:

  X-axis:
    ┌──────────────────────────────────┐
    │ @timestamp                       │
    │ Date Histogram (auto interval)   │
    └──────────────────────────────────┘
    
  Y-axis:
    ┌──────────────────────────────────┐
    │ performance.latency_ms           │
    │ Range: 0 to 10 (step: 1)         │
    └──────────────────────────────────┘
    
  Cell value:
    ┌──────────────────────────────────┐
    │ Count                            │
    └──────────────────────────────────┘

Step 4: [Save] → Title: "Latency Distribution Heatmap"
```

**Expected Result:**
```
Latency
 9ms │  ░░  ░░  ░░  ░░
 8ms │  ░░  ░░  ░░  ░░
 7ms │  ░░  ░░  ░░  ░░
 6ms │  ░░  ░░  ░░  ░░
 5ms │  ░░  ░░  ░░  ░░
 4ms │  ░░  ░░  ░░  ░░
 3ms │  ░░  ░░  ░░  ░░
 2ms │  ██  ░░  ░░  ░░
 1ms │  ██  ██  ██  ██      ← Most requests here (fast)
 0ms │  ██  ██  ██  ██
     └────────────────────► Time
```

**ဘာကိုပြတာလဲ:** ဒီ heatmap က latency ရဲ့ distribution ကိုပြတယ်။
အများစုက 1ms အောက်မှာရှိပြီး outlier တွေက 5ms+ မှာရှိတယ်ဆိုတာမြင်ရမယ်။

---

### 4.5 Visualization 5 — Top 10 Slowest Requests (Data Table)

**Purpose:** အနှေးဆုံး request တွေကိုအသေးစိတ်ကြည့်ဖို့

```
Step 1: ☰ → Analytics → Lens
Step 2: Visualization type → Table
Step 3: Configure:

  Columns:
    ┌──────────────────────────────────┐
    │ @timestamp        (Timestamp)    │
    │ request_id        (Request ID)   │
    │ prediction.label  (Label)        │
    │ performance.latency_ms (Latency) │
    │                     Sort: Desc   │
    └──────────────────────────────────┘

  Rows limit: 10

Step 4: [Save] → Title: "Slowest Requests"
```

**Expected Result:**
```
┌──────────────────┬──────────────────────┬───────┬─────────┐
│ Timestamp        │ Request ID           │ Label │ Latency │
├──────────────────┼──────────────────────┼───────┼─────────┤
│ 2026-06-30T14:30 │ a1b2c3d4-...        │ 0     │ 2.134ms │
│ 2026-06-30T14:29 │ e5f6a7b8-...        │ 0     │ 1.892ms │
│ 2026-06-30T14:29 │ c9d0e1f2-...        │ 1     │ 1.567ms │
│ ...              │ ...                  │ ...   │ ...     │
└──────────────────┴──────────────────────┴───────┴─────────┘
```

**ဘာကိုပြတာလဲ:** ဒီ table က အနှေးဆုံး request တွေရဲ့အသေးစိတ်ကိုပြတယ်။
ဘယ် request က ဘာကြောင့်နှေးတာလဲဆိုတာ request_id နဲ့ခြေရာခံလို့ရတယ်။

---

### 4.6 Visualization 6 — Model Performance Over Time (Line Chart)

**Purpose:** Accuracy, latency percentiles တွေက time နဲ့အမျှဘယ်လိုပြောင်းလဲလဲ

```
Step 1: Create a NEW Data View for ml-metrics:
    Name: ML Metrics
    Index pattern: ml-metrics*
    Timestamp: @timestamp

Step 2: ☰ → Analytics → Lens
Step 3: Visualization type → Line chart
Step 4: Configure:

  X-axis:
    ┌──────────────────────────────────┐
    │ @timestamp (Date Histogram)      │
    └──────────────────────────────────┘
    
  Y-axis (multiple lines):
    ┌──────────────────────────────────┐
    │ Line 1: performance.accuracy     │
    │         Average                  │
    │         Label: "Accuracy"        │
    │                                  │
    │ Line 2: performance.f1_score     │
    │         Average                  │
    │         Label: "F1 Score"        │
    │                                  │
    │ Line 3: performance.p95_latency  │
    │         Average                  │
    │         Label: "P95 Latency"     │
    └──────────────────────────────────┘

Step 5: [Save] → Title: "Model Performance Over Time"
```

**ဘာကိုပြတာလဲ:** ဒီ line chart က model performance metrics တွေရဲ့
trend ကိုပြတယ်။ Accuracy ကျလာရင်၊ latency များလာရင် သိနိုင်တယ်။

---

### 4.7 Visualization 7 — Confidence Distribution (Histogram)

**Purpose:** Model confidence ရဲ့ distribution ကိုကြည့်ဖို့

```
Step 1: ☰ → Analytics → Lens
Step 2: Visualization type → Bar chart (horizontal)
Step 3: Configure:

  X-axis:
    ┌──────────────────────────────────┐
    │ prediction.confidence            │
    │ Intervals: 10 (0.0, 0.1, ... 1.0)│
    └──────────────────────────────────┘
    
  Y-axis:
    ┌──────────────────────────────────┐
    │ Count                            │
    └──────────────────────────────────┘
    
  Breakdown:
    ┌──────────────────────────────────┐
    │ prediction.label_index           │
    │ (split bars by label)            │
    └──────────────────────────────────┘

Step 4: [Save] → Title: "Confidence Distribution"
```

**Expected Result:**
```
Confidence
1.0  │  ████████████████████████  ← Most predictions at 100% confidence
0.9  │  ░░
0.8  │  ░░
0.7  │  ░░
...  │  ░░
     └──────────────────────► Count
```

**ဘာကိုပြတာလဲ:** Model က ဘယ်လောက် confident ရှိလဲဆိုတာကိုပြတယ်။
Confidence 0.9+ မှာအများစုရှိသင့်တယ် — confidence နည်းတဲ့ predictions တွေ
များလာရင် model က uncertainty များနေတယ်လို့သိနိုင်တယ်။

---

### 4.8 Visualization 8 — Feature Values Over Time (Scatter Plot)

**Purpose:** Input features တွေရဲ့ distribution ကိုကြည့်ဖို့ (drift detection visual)

```
Step 1: ☰ → Analytics → Lens
Step 2: Visualization type → Scatter plot
Step 3: Configure:

  X-axis:
    ┌──────────────────────────────────┐
    │ @timestamp                       │
    └──────────────────────────────────┘
    
  Y-axis:
    ┌──────────────────────────────────┐
    │ input_features.features[0]       │
    │ (ဒါမှမဟုတ် သင်စိတ်ဝင်စားတဲ့ feature)│
    └──────────────────────────────────┘
    
  Point size:
    ┌──────────────────────────────────┐
    │ Count                            │
    └──────────────────────────────────┘

Step 4: [Save] → Title: "Feature: amount Over Time"
```

**ဘာကိုပြတာလဲ:** ဒီ scatter plot က feature တန်ဖိုးတွေရဲ့ distribution ကို
အချိန်နဲ့အမျှပြတယ်။ Feature တန်ဖိုးတွေ ရုတ်တရက်ပြောင်းသွားရင်
(data drift) မြင်နိုင်တယ်။

---

## 5. Dashboard ဆောက်ခြင်း

Visualization တွေအကုန်ဆောက်ပြီးရင် Dashboard ထဲမှာစုစည်းမယ်။

```
Step 1: ☰ → Analytics → Dashboard

Step 2: [Create dashboard]

Step 3: [Add from library]
    ┌─────────────────────────────────────────────┐
    │ အောက်ပါတို့ကိုရွေးပါ:                        │
    │                                             │
    │ ☑ Predictions Over Time                     │
    │ ☑ Fraud vs Non-Fraud                        │
    │ ☑ Average Inference Latency                 │
    │ ☑ Latency Distribution Heatmap              │
    │ ☑ Slowest Requests                          │
    │ ☑ Model Performance Over Time               │
    │ ☑ Confidence Distribution                   │
    │ ☑ Feature: amount Over Time                 │
    │                                             │
    │ [Add]                                       │
    └─────────────────────────────────────────────┘

Step 4: Dashboard Layout ချိန်ညှိခြင်း
    ┌────────────────────────────────────────────────────────┐
    │ Row 1:  [Predictions Over Time       ][Fraud vs Fraud]│
    │         (full width bar chart)       (pie chart)      │
    ├────────────────────────────────────────────────────────┤
    │ Row 2:  [Avg Latency ][Latency Heatmap    ]            │
    │         (metric)     (heatmap)                         │
    ├────────────────────────────────────────────────────────┤
    │ Row 3:  [Slowest Requests Table                   ]    │
    │         (data table)                                   │
    ├────────────────────────────────────────────────────────┤
    │ Row 4:  [Model Performance Over Time             ]    │
    │         (line chart with accuracy, f1, latency)        │
    ├────────────────────────────────────────────────────────┤
    │ Row 5:  [Confidence ][Feature: amount Over Time]       │
    │         (histogram) (scatter)                          │
    └────────────────────────────────────────────────────────┘

Step 5: Time range သတ်မှတ်ပါ
    ┌──────────────────────────────────┐
    │ 右上の time picker:               │
    │  📅 Last 15 minutes              │
    │  (ဒါမှမဟုတ် Last 1 hour)         │
    └──────────────────────────────────┘

Step 6: [Save] → Title: "ML Inference Monitoring Dashboard"
```

---

## 6. Dashboard Auto-Refresh သတ်မှတ်ခြင်း

Dashboard ကို အလိုအလျောက် refresh ဖြစ်အောင်လုပ်ပါ:

```
Step 1: Dashboard ထဲမှာ အပေါ်နားက [Refresh] ခလုတ်ဘေးက
        နာရီပုံလေးကိုနှိပ်ပါ

Step 2: Set refresh interval:
    ┌──────────────────────────────────┐
    │  Refresh every:                  │
    │  ○ Off                           │
    │  ○ 5 seconds                     │
    │  ● 30 seconds  ← ဒါကိုရွေးပါ     │
    │  ○ 1 minute                      │
    │  ○ 5 minutes                     │
    │  ○ 15 minutes                    │
    └──────────────────────────────────┘
```

**ရှင်းလင်းချက်:** Auto-refresh က dashboard ကို စက္ကန့် ၃၀ တစ်ခါ
အလိုအလျောက် update လုပ်ပေးတယ်။ ဒါကြောင့် real-time monitoring လုပ်လို့ရတယ်။

---

## 7. Dashboard တစ်ခုလုံးရဲ့ပုံစံ

အဆင့်တွေအကုန်လုပ်ပြီးရင် dashboard က ဒီလိုမျိုးဖြစ်နေမယ်:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 ML Inference Monitoring Dashboard              🔄 Auto-refresh│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────┐  ┌──────────────────┐   │
│  │                                     │  │                  │   │
│  │   Predictions Over Time             │  │ Fraud vs Non-    │   │
│  │   ██                               │  │ Fraud            │   │
│  │   ██ ██                            │  │    ╭─────╮       │   │
│  │   ██ ██ ██                         │  │   ╱ Fraud ╲      │   │
│  │   ██ ██ ██ ██                      │  │  │  16%   │      │   │
│  └─────────────────────────────────────┘  └──────────────────┘   │
│                                                                  │
│  ┌────────────────────┐  ┌────────────────────────────────────┐  │
│  │ ╔══════════════╗   │  │ Latency Distribution Heatmap       │  │
│  │ ║  0.711 ms    ║   │  │  ██░░░░░░░░░░░░░░░░░░░░░░░░░      │  │
│  │ ║ Avg Latency  ║   │  │  ██░░░░░░░░░░░░░░░░░░░░░░░░░      │  │
│  │ ╚══════════════╝   │  └────────────────────────────────────┘  │
│  └────────────────────┘                                          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Slowest Requests                                             │ │
│  │ ┌────────┬──────────────────────┬───────┬─────────┐        │ │
│  │ │ Time   │ Request ID           │ Label │ Latency │        │ │
│  │ ├────────┼──────────────────────┼───────┼─────────┤        │ │
│  │ │ 14:30  │ a1b2c3d4-...        │ 0     │ 2.134ms │        │ │
│  │ │ 14:29  │ e5f6a7b8-...        │ 0     │ 1.892ms │        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Model Performance Over Time                                  │ │
│  │ 1.0 ──────────────────────── Accuracy                       │ │
│  │ 0.8 ──────────────────────── F1 Score                       │ │
│  │ 0.6                                                          │ │
│  │ 0.4                                                          │ │
│  │ 0.2 ──────── P95 Latency (right axis)                       │ │
│  │ 0.0 ────────────────────────────────────────────► Time      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────┐  ┌────────────────────────────────────┐  │
│  │ Confidence Dist    │  │ Feature: amount Over Time          │  │
│  │ ████████████████   │  │  ⬤                                │  │
│  │ ░░░░░░░░░░░░░░░░   │  │    ⬤      ⬤                       │  │
│  │ 0.5      1.0       │  │      ⬤  ⬤    ⬤                    │  │
│  └────────────────────┘  └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. အသုံးဝင်သော Kibana Queries (Discover မှာ)

Kibana **Discover** မှာ ဒီ queries တွေသုံးပြီး data တွေကိုရှာနိုင်တယ်:

### 8.1 Fraud Predictions အကုန်ရှာရန်

```
prediction.label_index: 1
```

### 8.2 နှေးတဲ့ Requests (2ms ကျော်)

```
performance.latency_ms: > 2
```

### 8.3 Error ဖြစ်တဲ့ Requests

```
status: error
```

### 8.4 လွန်ခဲ့တဲ့ ၅ မိနစ်အတွင်း Requests

```
@timestamp: now-5m
```

### 8.5 Confidence 90% အောက် Requests

```
prediction.confidence: < 0.9
```

### 8.6 Combined Query (fraud + နှေး)

```
prediction.label_index: 1 AND performance.latency_ms: > 1
```

---

## 9. Advanced: Dashboard URL ကို Sharing လုပ်ခြင်း

### 9.1 Dashboard ID ရယူရန်

```
Dashboard URL က ဒီလိုပုံစံဖြစ်တယ်:
http://192.168.1.122:5601/app/dashboards#/view/abc12345-xxxx-xxxx-xxxx-xxxxxxxxxxxx

abc12345-xxxx-xxxx-xxxx-xxxxxxxxxxxx = Dashboard ID
```

### 9.2 Embedding (iFrame)

Kibana → Dashboard → Share → Embed code

```html
<iframe src="http://192.168.1.122:5601/app/dashboards#/view/abc12345-xxxx-xxxx?embed=true"
  height="600" width="800"></iframe>
```

---

## 10. Alerts သတ်မှတ်ခြင်း (Optional)

Kibana Alerts ကို သုံးပြီး threshold-based alerts တွေထားလို့ရတယ်:

```
Step 1: ☰ → Stack Management → Rules & Connectors

Step 2: [Create rule]
    ┌──────────────────────────────────┐
    │  Rule type: Elasticsearch query   │
    │                                   │
    │  Index: ml-inference*             │
    │  Query:                           │
    │    performance.latency_ms: > 5    │
    │                                   │
    │  Check every: 1 minute            │
    │                                   │
    │  Actions:                         │
    │  ☐ Slack webhook (if configured)  │
    │  ☐ Email                          │
    └──────────────────────────────────┘

    Rule name: "High Latency Alert"
```

**အကြံပြုချက် — အရေးကြီးဆုံး Alerts:**

| Alert Name | ES Query | Threshold | Severity |
|-----------|----------|-----------|----------|
| High Latency | `performance.latency_ms: > 5` | >5ms for 10 requests | Warning |
| Error Rate | `status: error` | >5% in 5 min | Critical |
| No Data | (index empty) | 0 docs in 5 min | Critical |
| Fraud Spike | `prediction.label_index: 1` | >20% in 5 min | Info |

---

## 11. Dashboard Maintenance

### 11.1 Data Retention

`ml-inference` index က auto-create ဖြစ်တယ် — ILM policy မရှိရင်
data တွေက indefinite ရှိနေမယ်။ Production မှာ ILM ထည့်သင့်တယ်:

```bash
curl -u elastic:'ML0psElk!2026' -X PUT "http://192.168.1.123:80/_ilm/policy/ml-logs-policy" \
  -H "Content-Type: application/json" \
  -d '{
    "policy": {
      "phases": {
        "hot": {
          "min_age": "0d",
          "actions": {
            "rollover": {
              "max_size": "10GB",
              "max_age": "7d"
            }
          }
        },
        "delete": {
          "min_age": "30d",
          "actions": {
            "delete": {}
          }
        }
      }
    }
  }'
```

### 11.2 Dashboard Export/Import

Dashboard ကို export/import လုပ်ဖို့:

```
Export:
  ☰ → Stack Management → Saved Objects
  → Search "ML Inference"
  → Select all related objects
  → [Export]

Import:
  ☰ → Stack Management → Saved Objects
  → [Import]
  → Select the .ndjson file
```

---

## 12. ဘာတွေလေ့လာနိုင်လဲ (Summary)

ဒီ Lab ကနေ သင်တတ်မြောက်သွားတဲ့အချက်များ:

| # | သင်ခန်းစာ | ရှင်းလင်းချက် |
|---|-----------|----------------|
| 1 | Data View ဆောက်ခြင်း | ES index ကို Kibana နဲ့ချိတ်ဆက်နည်း |
| 2 | Lens Visualization | Bar, Pie, Metric, Heatmap, Table, Line, Scatter |
| 3 | Dashboard Layout | Visualization တွေကိုစုစည်းပြီး layout ချနည်း |
| 4 | Auto-Refresh | Dashboard ကို အလိုအလျောက် update လုပ်နည်း |
| 5 | ES Queries | Discover မှာ data ရှာဖွေနည်း |
| 6 | Alerts | Threshold-based alert သတ်မှတ်နည်း |
| 7 | ILM Policy | Data retention စီမံခန့်ခွဲနည်း |

**အဆင့်ဆင့်လေ့လာရန်:**

```
ML Model Training → Server Start → Send Requests → ES Index
                                                        │
                                                        ▼
                                                    Kibana Dashboard
                                                        │
                                              ┌─────────┴─────────┐
                                              ▼                   ▼
                                        Visualizations        Alerts
                                        (bar, pie, etc.)     (Slack, email)
                                              │
                                              ▼
                                        Monitor & Improve
                                        (Drift, Accuracy, Latency)
```

---

*End of Kibana Dashboard Guide*

© 2026 ML Inference Service — MLOps Learning Series
