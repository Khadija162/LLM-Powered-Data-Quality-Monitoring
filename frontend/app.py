import os
import requests
import streamlit as st
st.set_page_config(page_title="AI Data Quality Control Center", layout="wide")
st.title("AI Data Quality · Control Center")
st.caption("Bronze → Silver → Gold · Open data · Read-only incident explanation")
api = os.getenv("API_URL", "http://localhost:8000")
try:
    response = requests.get(api + "/api/metrics", timeout=5)
    response.raise_for_status()
    report = response.json().get("report")
except requests.RequestException:
    report = None
if report:
    a, b, c = st.columns(3)
    a.metric("Raw rows", report["bronze_count"])
    b.metric("Valid rows", report["silver_count"])
    c.metric("Rejected", report["rejected_count"])
    st.subheader("Quality alerts")
    st.json(report["alerts"])
    if st.button("Explain incident with LLM"):
        try:
            result = requests.post(api + "/api/incidents/explain", timeout=120)
            result.raise_for_status()
            st.json(result.json())
        except requests.RequestException as exc:
            st.error(str(exc))
else:
    st.info("No report yet. Run the data-quality pipeline first.")
