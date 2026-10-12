import pandas as pd
from fastapi.testclient import TestClient
from backend.main import app
from quality.pipeline import run
from quality.llm import analyze


def test_pipeline(tmp_path):
    frame = pd.DataFrame({
        "sepal length (cm)": [5.1, -2], "sepal width (cm)": [3.5, 3.2],
        "petal length (cm)": [1.4, 1.4], "petal width (cm)": [0.2, 0.2],
        "target": [0, 0]
    })
    csv = tmp_path / "source.csv"
    frame.to_csv(csv, index=False)
    result = run(str(csv), str(tmp_path / "lake"), str(tmp_path / "reports"))
    assert result["rejected_count"] == 1
    assert result["silver_count"] == 1
    assert result["alerts"][0]["rule"] == "REJECTION_RATE"


def test_mock(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "mock")
    result = analyze({"bronze_count": 10, "silver_count": 9, "rejected_count": 1, "rejection_rate": 10, "alerts": []})
    assert result["approved"] is False


def test_health():
    assert TestClient(app).get("/health").status_code == 200
