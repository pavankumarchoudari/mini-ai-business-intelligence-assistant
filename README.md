# Mini AI Business Intelligence Assistant

A small application that lets a business user ask natural-language questions about sales data. The application interprets the question, runs a predefined read-only SQL query against SQLite, and returns an answer with supporting figures.

## Features
- Imports the supplied CSV using Pandas and stores cleaned records in SQLite.
- Supports total revenue, highest-revenue product, monthly trend, highest-sales region, and two-month revenue comparison.
- Uses Groq LLM optionally for intent classification. Without an API key or network access, a deterministic local intent parser is used.
- The LLM does not generate or execute SQL. The backend selects from predefined read-only queries.
- FastAPI backend and Streamlit frontend.
- Automated tests with Pytest.

## Data rules and revenue definition
- Include records whose status is `Completed`.
- Exclude records with invalid dates, missing required values, non-positive quantity, non-positive unit price, or negative discount.
- `Gross_revenue = Quantity * Unit_price`.
- `Net_revenue = Gross_revenue - Discount_amount`.
- `Discount_amount` is treated as a transaction-level amount, not a per-unit discount.
- The original CSV is retained unchanged in `data/sales_data.csv`.

## Architecture
`User question -> Streamlit UI -> FastAPI -> Intent interpreter -> allowlisted analytics function -> SQLite -> structured result -> UI`

The intent interpreter returns one of five supported intents. SQL is fixed in `backend/analytics.py`; user text is never concatenated into SQL. Month parameters use placeholders (`?`). The database connection is used only for SELECT analytics in the question path.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the application

Open two terminals in the project folder. Activate `.venv` in both.

Terminal 1 – backend:
```powershell
uvicorn backend.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

Terminal 2 – frontend:
```powershell
streamlit run frontend/app.py
```
Open the local Streamlit URL shown in the terminal (usually http://localhost:8501).

## Optional Groq AI configuration
The app runs without a key. To enable LLM-based intent classification:
1. Create a `.env` file in the project root (never commit it).
2. Add `GROQ_API_KEY=your_key`.
3. Install/use the Groq package already listed in requirements.
4. Export the variable in the terminal before starting FastAPI:
```powershell
$env:GROQ_API_KEY="your_key"
uvicorn backend.main:app --reload
```
If the API is unavailable, the application falls back to deterministic rules. The LLM only classifies intent; calculations always come from SQL.

## Supported example questions
- What is the total revenue?
- Which product generated the highest revenue?
- What is the monthly revenue trend?
- Which region generated the highest sales?
- Compare January 2026 and February 2026 revenue.

For comparisons, use month names and years, e.g. `Compare March 2026 and April 2026 revenue`.

## Tests
```powershell
pytest -q
```
Tests cover analytics queries, intent interpretation, unsupported requests, and month comparisons.

## API
- `GET /health`
- `GET /data-quality`
- `POST /ask` with JSON body: `{"question":"What is the total revenue?"}`

## Known limitations
- This prototype supports five predefined analytical intents, not arbitrary business questions.
- The local rules parser recognizes common phrasings; the optional LLM improves phrasing flexibility.
- Month comparison assumes 2026 when a year is omitted.
- Authentication, multi-user access, deployment hardening, and large-dataset optimization are outside the assessment scope.

## AI-assisted development and reflection
See `docs/development_notes.md`. Update it with the actual prompts, issues, and debugging steps from your own development session before submission.
