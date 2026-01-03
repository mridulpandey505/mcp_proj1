import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score


MODEL_PATH = "resources/models/churn_model.pkl"


def train_model(dataset_path: str):
    """
    Train a churn prediction model and save it as an artifact.
    """

    # Load dataset
    dataset_path = "resources/datasets/churn_data.csv"
    df = pd.read_csv(dataset_path)
    TARGET_COL = "churn"
    if TARGET_COL not in df.columns:
        raise ValueError(f"Target column '{TARGET_COL}' not found")

    # Split features & target
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 3),
        "precision": round(precision_score(y_test, y_pred), 3),
        "recall": round(recall_score(y_test, y_pred), 3)
    }

    # Save model
    joblib.dump(model, MODEL_PATH)

    return {
        "status": "model_trained",
        "model_path": MODEL_PATH,
        "metrics": metrics
    }


def predict_churn(dataset_path: str):
    """
    Run churn prediction using a trained model.
    """

    # Load model
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        raise RuntimeError(
            "Model not found. Train the model before prediction."
        )

    # Load dataset
    df = pd.read_csv(dataset_path)

    TARGET_COLUMN = "churn"

    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Required column '{TARGET_COLUMN}' not found in dataset. "
            f"Available columns: {list(df.columns)}"
        )

    X = df.drop(columns=[TARGET_COLUMN])

    predictions = model.predict(X)

    churn_rate = float((predictions == 1).mean())

    return {
        "total_records": len(predictions),
        "predicted_churn_count": int((predictions == 1).sum()),
        "churn_rate": round(churn_rate, 3)
    }
