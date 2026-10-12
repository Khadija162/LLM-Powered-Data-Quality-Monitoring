"""Reproducible public-data quality pipeline; Bronze/Silver/Gold Parquet and JSON reports."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import duckdb

REQUIRED = ("sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)", "target")


def run(source="data/public/iris.csv", root="data", reports="artifacts"):
    frame = pd.read_csv(source)
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    root = Path(root)
    for layer in ("bronze", "silver", "gold"):
        (root / layer).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(root / "bronze" / "iris.parquet", index=False)
    numeric = frame[list(REQUIRED)].apply(pd.to_numeric, errors="coerce")
    valid = numeric.notna().all(axis=1)
    valid &= numeric[list(REQUIRED[:4])].gt(0).all(axis=1)
    valid &= numeric["target"].isin([0, 1, 2])
    valid &= ~numeric.duplicated(keep="first")
    clean = frame.loc[valid].copy()
    rejected = frame.loc[~valid].copy()
    clean.to_parquet(root / "silver" / "iris.parquet", index=False)
    rejected.to_parquet(root / "silver" / "rejected.parquet", index=False)
    with duckdb.connect() as conn:
        gold = conn.execute(
            "SELECT target, count(*) AS records, avg(\"sepal length (cm)\") AS avg_sepal_length "
            "FROM read_parquet(?) GROUP BY target ORDER BY target",
            [str((root / "silver" / "iris.parquet").as_posix())],
        ).df()
    gold.to_parquet(root / "gold" / "summary.parquet", index=False)
    metrics = {"timestamp": datetime.now(timezone.utc).isoformat(),
               "source": "Iris, UCI Machine Learning Repository (CC BY 4.0)",
               "bronze_count": int(len(frame)), "silver_count": int(len(clean)),
               "rejected_count": int(len(rejected)),
               "rejection_rate": round(float(len(rejected) / len(frame)) * 100, 2) if len(frame) else 0.0,
               "alerts": []}
    if len(rejected) / max(len(frame), 1) > .05:
        metrics["alerts"].append({"severity": "CRITICAL", "rule": "REJECTION_RATE", "message": "More than 5% of rows rejected"})
    if len(frame) == 0:
        metrics["alerts"].append({"severity": "WARNING", "rule": "EMPTY_SOURCE", "message": "Source dataset empty"})
    report_path = Path(reports) / "latest.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="data/public/iris.csv")
    args = p.parse_args()
    print(json.dumps(run(args.source), indent=2))
