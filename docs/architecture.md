# Architecture and maturity

Implemented: UCI Iris acquisition from open upstream source, Pandas/Parquet Bronze/Silver/Gold pipeline, DuckDB analytics, rule-based quality checks and JSON incident reports, Ollama open-weight model interface (mock default), FastAPI backend, Streamlit UI, tests, Docker and GitHub Actions.

Not implemented: live Spark/Delta streaming, Azure Container Apps, production role-based access, Azure Data Factory, Azure Monitor, real Azure-hosted LLM, scheduled ingestion or model quality evaluation.

Azure roadmap: Data Factory or Event Hubs ingestion -> ADLS Gen2 -> Azure Databricks (Spark/Delta) -> monitoring tables in Azure Database for PostgreSQL -> FastAPI and Streamlit Container Apps -> open-weight LLM serving via managed GPU endpoint -> Azure Monitor and Key Vault.

Security: No autonomous remediation; incident explanation only. Documents and data are untrusted evidence. Do not expose the unauthenticated API to the public internet. Keep model endpoints and secrets server-side. Terraform is just storage infrastructure and is not applied automatically.
