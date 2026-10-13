from pathlib import Path
import json
import warnings

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from features import make_feature_frame

warnings.filterwarnings("ignore", category=UserWarning)
ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)

def load_dataset():
    """Fetches UCI PhiUSIIL dataset. Internet access is needed the first time."""
    from ucimlrepo import fetch_ucirepo
    dataset = fetch_ucirepo(id=967)
    X_raw = dataset.data.features
    y_raw = dataset.data.targets

    # Locate the URL column and label column without assuming exact capitalization.
    url_col = next((c for c in X_raw.columns if str(c).strip().lower() == "url"), None)
    if url_col is None:
        raise ValueError(f"Could not find a URL column. Available columns: {list(X_raw.columns)}")

    y_col = next((c for c in y_raw.columns if str(c).strip().lower() in {"label", "result", "target", "class"}), None)
    if y_col is None:
        if y_raw.shape[1] != 1:
            raise ValueError(f"Could not identify target column: {list(y_raw.columns)}")
        y_col = y_raw.columns[0]

    data = pd.DataFrame({"url": X_raw[url_col].astype(str), "label": y_raw[y_col]})
    data = data.dropna().drop_duplicates(subset=["url"]).reset_index(drop=True)
    # PhiUSIIL uses 1 = legitimate and 0 = phishing. Convert to phishing=1 for the app.
    labels = pd.to_numeric(data["label"], errors="coerce")
    valid = labels.isin([0, 1])
    data = data.loc[valid].copy()
    data["label"] = (labels.loc[valid] == 0).astype(int).values
    return data

def main():
    print("Downloading/loading UCI PhiUSIIL dataset...")
    data = load_dataset()
    print(f"Records after basic cleaning: {len(data):,}")
    print("Extracting URL-only features...")
    X = make_feature_frame(data["url"].tolist())
    y = data["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
        "Decision Tree": DecisionTreeClassifier(max_depth=12, class_weight="balanced", random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=None, min_samples_leaf=2,
            class_weight="balanced_subsample", random_state=42, n_jobs=-1
        ),
    }

    results = []
    fitted = {}
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        try:
            proba = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, proba)
        except Exception:
            auc = float("nan")
        row = {
            "model": name,
            "accuracy": accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1_score": f1_score(y_test, pred, zero_division=0),
            "roc_auc": auc,
            "tn_fp_fn_tp": confusion_matrix(y_test, pred, labels=[0, 1]).ravel().tolist()
        }
        results.append(row)
        fitted[name] = model
        print(
            f"  accuracy={row['accuracy']:.4f}, precision={row['precision']:.4f}, "
            f"recall={row['recall']:.4f}, F1={row['f1_score']:.4f}, AUC={row['roc_auc']:.4f}"
        )

    # Prioritize F1 as a balance of precision and recall; discuss recall due to phishing risk.
    best_row = max(results, key=lambda item: item["f1_score"])
    best_model = fitted[best_row["model"]]
    joblib.dump(
        {"model": best_model, "feature_names": list(X.columns),
         "best_model_name": best_row["model"], "positive_label": "phishing"},
        ARTIFACTS / "phishing_model.joblib"
    )
    with open(ARTIFACTS / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    pd.DataFrame(results).drop(columns=["tn_fp_fn_tp"]).to_csv(ARTIFACTS / "model_comparison.csv", index=False)
    print(f"\nBest model by F1-score: {best_row['model']}")
    print(f"Saved model to: {ARTIFACTS / 'phishing_model.joblib'}")
    print(f"Saved metrics to: {ARTIFACTS / 'model_comparison.csv'}")

if __name__ == "__main__":
    main()
