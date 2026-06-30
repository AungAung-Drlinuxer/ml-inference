"""
ml-inference / app / train_model.py

Trains a fraud-detection pipeline on raw feature vectors (no named columns).
The model only applies RobustScaler + classifier, so it accepts a flat
List[float] at inference time — no DataFrame needed.
"""

import os
import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
logger = logging.getLogger("train_model")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")


def generate_sample_data(n: int = 10_000, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic payment-fraud data (same schema as before)."""
    rng = np.random.default_rng(seed)
    amount = np.round(np.exp(rng.uniform(1, 10, n)), 2)
    oldbalanceOrg = np.round(amount * rng.uniform(0.5, 5.0, n), 2)
    newbalanceOrig = np.round(oldbalanceOrg - amount * rng.uniform(0.8, 1.2, n), 2)
    newbalanceOrig = np.clip(newbalanceOrig, 0, None)
    oldbalanceDest = np.round(np.exp(rng.uniform(1, 12, n)), 2)
    newbalanceDest = np.round(oldbalanceDest + amount * rng.uniform(0.8, 1.2, n), 2)
    is_fraud = np.zeros(n, dtype=int)
    fraud_mask = rng.random(n) < 0.008
    n_fraud = fraud_mask.sum()
    amount[fraud_mask] = np.round(rng.uniform(5000, 50000, n_fraud), 2)
    oldbalanceOrg[fraud_mask] = np.round(rng.uniform(10000, 200000, n_fraud), 2)
    newbalanceOrig[fraud_mask] = 0.0
    is_fraud[fraud_mask] = 1
    df = pd.DataFrame({
        "amount": amount, "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig, "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest, "isFraud": is_fraud,
    })
    logger.info("Generated %d rows (fraud rate = %.4f)", n, df["isFraud"].mean())
    return df


def train():
    logger.info("Training fraud-detection model (raw vector pipeline)...")

    # Generate data
    df = generate_sample_data()

    # Feature matrix: order matches what main.py sends as List[float]
    FEATURE_COLS = ["amount", "oldbalanceOrg", "newbalanceOrig",
                    "oldbalanceDest", "newbalanceDest"]
    X = df[FEATURE_COLS].values  # numpy array, no column names
    y = df["isFraud"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )

    # Simple pipeline: scale then classify — NO ColumnTransformer
    from sklearn.pipeline import Pipeline
    pipeline = Pipeline([
        ("scaler", RobustScaler()),
        ("classifier", GradientBoostingClassifier(
            n_estimators=150, max_depth=4, learning_rate=0.1,
            subsample=0.8, random_state=42,
        )),
    ])

    pipeline.fit(X_train, y_train)
    train_acc = pipeline.score(X_train, y_train)
    test_acc = pipeline.score(X_test, y_test)
    logger.info("Train accuracy: %.4f", train_acc)
    logger.info("Test accuracy:  %.4f", test_acc)

    # Verify it works with raw numpy array (as List[float] would produce)
    sample = X_test[0:1]
    pred = int(pipeline.predict(sample)[0])
    proba = pipeline.predict_proba(sample)[0].tolist()
    logger.info("Sample pred=%d proba=%s", pred, proba)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    logger.info("Model saved to %s", MODEL_PATH)

    # Save reference slice for drift detection
    ref_path = os.path.join(os.path.dirname(__file__), "..", "data", "reference.csv")
    df[FEATURE_COLS].head(1000).to_csv(ref_path, index=False)
    logger.info("Reference data saved to %s", ref_path)


if __name__ == "__main__":
    train()
