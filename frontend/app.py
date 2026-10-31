import os
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Business Intelligence Assistant", page_icon="📊", layout="wide")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("📊 Mini AI Business Intelligence Assistant")
st.caption("Ask questions about sales transactions in natural language. Answers are calculated from SQLite data.")

with st.sidebar:
    st.header("Try these questions")
    examples = [
        "What is the total revenue?",
        "Which product generated the highest revenue?",
        "What is the monthly revenue trend?",
        "Which region generated the highest sales?",
        "Compare January 2026 and February 2026 revenue."
    ]
    for example in examples:
        st.code(example, language=None)
    st.divider()
    st.caption("Revenue = quantity × unit price − transaction discount. Only valid Completed transactions are included.")

try:
    health = requests.get(f"{API_URL}/health", timeout=3)
    health.raise_for_status()
    st.success("Backend connected")
except requests.RequestException:
    st.error("Cannot connect to the backend. Start FastAPI first: uvicorn backend.main:app --reload")
    st.stop()

question = st.text_input("Ask a sales question", placeholder="e.g. Which region generated the highest sales?")
if st.button("Get answer", type="primary") and question.strip():
    try:
        response = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=30)
        if response.ok:
            result = response.json()
            st.subheader("Answer")
            st.write(result["answer"])
            st.caption(f"Detected intent: {result['intent']} · Interpretation: {result['interpretation_method']}")
            st.subheader("Supporting figures")
            data = result["data"]
            if isinstance(data, list):
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                if "month" in df.columns and "net_revenue" in df.columns:
                    st.line_chart(df.set_index("month")["net_revenue"])
            else:
                st.json(data)
        else:
            st.warning(response.json().get("detail", "The request could not be processed."))
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
elif st.button("Show data quality summary"):
    try:
        summary = requests.get(f"{API_URL}/data-quality", timeout=10).json()
        st.json(summary)
    except requests.RequestException as exc:
        st.error(str(exc))

st.divider()
st.caption("Prototype for the AI-Assisted Development Challenge.")
