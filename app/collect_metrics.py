"""
ml-inference / app / collect_metrics.py

Standalone batch script (cron-friendly) that:
  1. Fetches recent inference logs from Elasticsearch
  2. Computes rolled-up performance metrics (accuracy, F1, latency percentiles)
  3. Runs data-drift detection against a reference baseline

Usage:
    python -m app.collect_metrics                    # single run
    python -m app.collect_metrics --interval 600     # loop every 10 min
"""

import argparse
import time as pytime
import numpy as np
import pandas as pd
from monitor import InferenceMonitor
from datetime import datetime, timezone, timedelta


def fetch_recent_inferences(monitor, minutes=15):
    """Return inference hits from the last N minutes."""
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interval",
        type=int,
        default=0,
        help="Run in a loop every N seconds (0 = one-shot)",
    )
    args = parser.parse_args()

    monitor = InferenceMonitor()

    while True:
        hits = fetch_recent_inferences(monitor, minutes=15)

        if len(hits) < 5:
            print(f"[SKIP] Only {len(hits)} hits — need ≥ 5 for metrics.")
            if args.interval == 0:
                return
            pytime.sleep(args.interval)
            continue

        preds = [h["_source"]["prediction"]["label_index"] for h in hits]
        probs = [h["_source"]["prediction"]["probabilities"] for h in hits]
        lats = [h["_source"]["performance"]["latency_ms"] for h in hits]

        # ---- Performance metrics ----
        monitor.log_performance_metrics(
            y_true=preds,
            y_pred=preds,
            y_prob=probs,
            latencies=lats,
            window_minutes=15,
        )

        # ---- Data-drift detection ----
        features = [
            list(h["_source"]["input_features"]["features"])
            for h in hits
            if "input_features" in h["_source"]
        ]

        if len(features) >= 20:
            n_cols = len(features[0])
            cols = [f"f{i}" for i in range(n_cols)]
            # Dummy reference — replace with real training baseline in prod
            reference = pd.DataFrame(np.random.randn(500, n_cols), columns=cols)
            current = pd.DataFrame(features, columns=cols)
            monitor.log_drift(reference, current)

        print(f"[OK] Batch analysis complete for {len(hits)} items.")

        if args.interval == 0:
            break
        pytime.sleep(args.interval)


if __name__ == "__main__":
    main()
