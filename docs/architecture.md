# Architecture

1. Streamlit collects a natural-language question.
2. Streamlit sends JSON to FastAPI `POST /ask`.
3. `ai_interpreter.py` classifies the request into an allowlisted intent. Groq is optional; deterministic rules are the fallback.
4. `analytics.py` executes a predefined SQL SELECT query against SQLite.
5. FastAPI returns an answer, intent, interpretation method, and supporting data.
6. Streamlit renders the answer and figures.

Safety: user question text is not inserted into SQL. Comparison months are passed as parameterized query values. No SQL-writing endpoint is exposed.
