import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from quality.llm import analyze
app = FastAPI(title="LLM Data Quality Monitoring", version="0.1.0")
REPORT = Path(os.getenv("REPORT_PATH", "artifacts/latest.json"))


@app.get("/health")
def health():
    return {"status": "ok", "report_available": REPORT.is_file()}


@app.get("/api/metrics")
def metrics():
    if not REPORT.is_file():
        return {"report": None}
    return {"report": json.loads(REPORT.read_text(encoding="utf-8"))}


@app.post("/api/incidents/explain")
def explain():
    if not REPORT.is_file():
        raise HTTPException(404, "Run quality pipeline first")
    try:
        return analyze(json.loads(REPORT.read_text(encoding="utf-8")))
    except (requests.RequestException, ValueError, KeyError) as exc:
        raise HTTPException(502, "LLM unavailable") from exc
