"""
ml-inference / app / monitor.py

Production inference monitor that logs every prediction request,
aggregated performance metrics, and data-drift reports to Elasticsearch.

Designed for use inside SageMaker endpoints, containers, or compute instances.
Environment variables control the ES connection settings so no code changes
are needed across environments.

Usage:
    from monitor import InferenceMonitor
    monitor = InferenceMonitor()
    monitor.log_inference(input_features={...}, prediction_label="fraud", ...)
    monitor.log_performance_metrics(y_true=[...], y_pred=[...], y_prob=[...], latencies=[...])
    monitor.log_drift(reference_df, current_df)
"""

import os
import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from typing import Optional

from elasticsearch import Elasticsearch


class InferenceMonitor:
    """
    Logs inference requests + aggregated metrics + drift reports
    to Elasticsearch for observability and MLOps auditing.

    Attributes
    ----------
    inference_index : str
        ES index for per-request inference logs.
    metrics_index   : str
        ES index for rolled-up performance & drift reports.
    """

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

        # --- Deployment metadata (injected via env) ---
        self.model_name = os.getenv("MODEL_NAME", "fraud-detector")
        self.model_version = os.getenv("MODEL_VERSION", "1.0.0")
        self.namespace = os.getenv("NAMESPACE", "ml-inference")
        self.pod_name = os.getenv("POD_NAME", "unknown")
        self.environment = os.getenv("ENVIRONMENT", "production")

    # ------------------------------------------------------------------
    #  1. Per-request inference logging
    # ------------------------------------------------------------------
    def log_inference(
        self,
        input_features: dict,
        prediction_label: str,
        prediction_index: int,
        probabilities: list,
        latency_ms: float,
        preprocessing_ms: float = 0.0,
        inference_ms: float = 0.0,
        postprocessing_ms: float = 0.0,
        status: str = "success",
        error_message: Optional[str] = None,
        client_ip: Optional[str] = None,
    ) -> None:
        """
        Send one inference log document to Elasticsearch.

        Parameters
        ----------
        input_features   : Raw feature dict sent by the client.
        prediction_label : Human-readable class name.
        prediction_index : Numeric class index.
        probabilities    : Softmax / sigmoid output list.
        latency_ms       : End-to-end wall-clock time.
        preprocessing_ms : Time spent in feature engineering.
        inference_ms     : Time spent inside model.predict().
        postprocessing_ms: Time spent converting output.
        status           : "success" | "error" | "stale".
        error_message    : Populated only on failure.
        client_ip        : Request origin (for audit).
        """
        confidence = float(max(probabilities)) if probabilities else 0.0

        doc = {
            "@timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": str(uuid.uuid4()),
            "model_name": self.model_name,
            "model_version": self.model_version,
            "pod_name": self.pod_name,
            "namespace": self.namespace,
            "environment": self.environment,
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

        if error_message:
            doc["error_message"] = error_message
        if client_ip:
            doc["client_ip"] = client_ip

        try:
            self.es.index(index=self.inference_index, document=doc)
        except Exception as e:
            # Never crash the serving path on a logging failure.
            print(f"[WARN] ES inference log failed: {e}")

    # ------------------------------------------------------------------
    #  2. Rolled-up performance metrics (called by the scheduler)
    # ------------------------------------------------------------------
    def log_performance_metrics(
        self,
        y_true: list,
        y_pred: list,
        y_prob: list,
        latencies: list,
        window_minutes: int = 15,
    ) -> None:
        """
        Compute classification metrics over a window and index them.

        This is the equivalent of a Grafana "accuracy over last 15 min"
        panel, but stored in ES so it can drive alerting rules or SLO
        dashboards.

        Parameters
        ----------
        y_true        : Ground-truth labels (collected via feedback loop).
        y_pred        : Predicted labels.
        y_prob        : Predicted probabilities (for log-loss).
        latencies     : Raw latency_ms values per request.
        window_minutes: Time window this batch covers.
        """
        from sklearn.metrics import (
            accuracy_score,
            f1_score,
            log_loss,
            precision_score,
            recall_score,
        )

        n = len(y_pred)
        if n < 5:
            return  # too small to be meaningful

        lat = np.array(latencies)

        perf = {
            "accuracy": round(accuracy_score(y_true, y_pred), 4),
            "precision": round(
                precision_score(y_true, y_pred, average="weighted", zero_division=0), 4
            ),
            "recall": round(
                recall_score(y_true, y_pred, average="weighted", zero_division=0), 4
            ),
            "f1_score": round(
                f1_score(y_true, y_pred, average="weighted", zero_division=0), 4
            ),
            "log_loss": round(log_loss(y_true, y_prob), 4) if y_prob else None,
            "total_predictions": n,
            "error_count": sum(1 for a, b in zip(y_true, y_pred) if a != b),
            "error_rate": round(
                sum(1 for a, b in zip(y_true, y_pred) if a != b) / n, 4
            ),
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
            print(
                f"[OK] Metrics logged — "
                f"acc={perf['accuracy']}, f1={perf['f1_score']}, "
                f"p95={perf['p95_latency_ms']}ms"
            )
        except Exception as e:
            print(f"[WARN] ES metrics log failed: {e}")

    # ------------------------------------------------------------------
    #  3. Data-drift detection (Evidently)
    # ------------------------------------------------------------------
    def log_drift(
        self, reference_df: pd.DataFrame, current_df: pd.DataFrame
    ) -> None:
        """
        Compare a current data window against a reference baseline and
        index the drift report into ES.

        Parameters
        ----------
        reference_df : Training / golden-baseline dataset.
        current_df   : Recent inference data to check for drift.
        """
        try:
            from evidently.report import Report
            from evidently.metric_preset import DataDriftPreset

            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=reference_df, current_data=current_df)
            result = report.as_dict()

            dr = result["metrics"][0]["result"]
            drifted = [
                col
                for col, val in dr.get("drift_by_columns", {}).items()
                if val.get("drift_detected")
            ]

            doc = {
                "@timestamp": datetime.now(timezone.utc).isoformat(),
                "model_name": self.model_name,
                "model_version": self.model_version,
                "environment": self.environment,
                "drift": {
                    "data_drift_score": round(
                        dr.get("share_of_drifted_columns", 0.0), 4
                    ),
                    "drift_detected": dr.get("dataset_drift", False),
                    "drifted_features": drifted,
                },
            }

            self.es.index(index=self.metrics_index, document=doc)
            print(f"[OK] Drift logged — detected={doc['drift']['drift_detected']}")
        except ImportError:
            print("[WARN] Evidently not installed — skipping drift check")
        except Exception as e:
            print(f"[WARN] Drift log failed: {e}")
