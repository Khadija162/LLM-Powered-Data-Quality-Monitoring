# LLM-Powered Data Quality Monitoring

**Open-data lakehouse quality observability + FastAPI backend + Streamlit frontend + open-weight Ollama incident analysis + Docker + GitHub Actions + Azure infrastructure starter.**

> **Implementation status:** Runnable local prototype with deterministic validation and mocked AI analysis. Ollama is optional. Azure resources, streaming ingestion, production authentication, scheduled monitoring and model evaluation are **not yet deployed**.

## Architecture

```text
UCI Iris (CC BY 4.0; included CSV)
       |
Batch ingestion -> Bronze Parquet -> Silver valid/rejected Parquet -> Gold DuckDB aggregates
                                       |
                                Quality metrics / alerts
                                       |
                                  JSON report
                                       |
                           FastAPI GET /api/metrics
                          FastAPI POST /api/incidents/explain
                                       |
                             Streamlit web dashboard
                                       |
                    Mock analyzer / optional local Ollama
```

## Public dataset and provenance

The included [Iris dataset](data/public/iris.csv) has 150 observations and comes from the UCI Machine Learning Repository, CC BY 4.0, DOI: https://doi.org/10.24432/C56C76 . The CSV was normalized from the [scikit-learn public Iris mirror](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/datasets/data/iris.csv). See [provenance](data/public/README.md). It is deliberately small and suited to reproducible demonstration, not production scale.

## Windows quick start

```powershell
git clone https://github.com/Khadija162/LLM-Powered-Data-Quality-Monitoring.git
cd LLM-Powered-Data-Quality-Monitoring
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m quality.pipeline
.\.venv\Scripts\python.exe -m pytest -q
```

If you want to refresh the public dataset:

```powershell
.\.venv\Scripts\python.exe -m quality.data
```

The report is written to `artifacts/latest.json`. Bronze/Silver/Gold files live in `data/` and are not committed.

Start the backend in terminal 1:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Start the frontend in terminal 2:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

API docs: http://localhost:8000/docs
Dashboard: http://localhost:8501

Or, after generating your local metrics report, launch Docker Desktop:

```powershell
docker compose up --build
```

## Open-weight LLM

The app uses `LLM_MODE=mock` by default. To enable local open-weight inference, install [Ollama](https://ollama.com/), pull a model and run the **host-side** backend:

```powershell
ollama pull qwen2.5:3b
$env:LLM_MODE="ollama"
$env:OLLAMA_MODEL="qwen2.5:3b"
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

The Docker Compose setup defaults to mock inference; running Ollama on the host does not automatically connect it to containers. **LLM output is advisory**, and must not alter data or validation rules without human review.

## Azure roadmap

Azure Data Factory / Event Hubs -> ADLS Gen2 -> Azure Databricks Delta Bronze/Silver/Gold -> Azure Database for PostgreSQL metrics -> Container Apps-hosted FastAPI/dashboard -> model serving on isolated GPU compute -> Azure Monitor / Key Vault / Entra ID.

Terraform in `infra/terraform/` currently declares an **Azure resource group and ADLS Gen2 storage only**. Nothing has been provisioned. Cloud resources may incur charges when deployed.

## Included directories

- `quality/` — public-data ingestion, lakehouse ETL, validations and Ollama adapter
- `backend/` — REST API to metrics and incident explanations
- `frontend/` — Streamlit dashboard
- `data/public/` — dataset and source attribution
- `tests/` — automated quality and API tests
- `.github/workflows/` — CI tests and Docker image build
- `infra/terraform/` — Azure storage example
- `docs/` — architecture and maturity

**Security:** No authentication is configured. Keep the demo bound to localhost; never publicly expose it without auth, least-privilege permissions and secrets management. The AI is read-only.
