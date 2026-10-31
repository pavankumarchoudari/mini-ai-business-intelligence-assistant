<div align="center">

# 🤖📊 Mini AI Business Intelligence Assistant

**Ask questions about your sales data in plain English and get answers backed by real database queries.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Tests](https://img.shields.io/badge/tests-15%20passed-brightgreen?style=for-the-badge)

### 🚀 [**Open the Live App**](https://mini-ai-business-intelligence-assistant-nvnaicqz6kc8ruzzrnfote.streamlit.app/)

[![Live Demo](https://img.shields.io/badge/▶_LIVE_DEMO-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://mini-ai-business-intelligence-assistant-nvnaicqz6kc8ruzzrnfote.streamlit.app/)
[![GitHub](https://img.shields.io/badge/SOURCE_CODE-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/pavankumarchoudari/mini-ai-business-intelligence-assistant)

</div>

> 💡 **Try it in 10 seconds:** open the live app and ask *"What is the total revenue?"* The expected answer is **₹14,39,200**. If the app has been idle, Streamlit Community Cloud may take a few seconds to wake it up.

---

## 📑 Table of Contents

1. [What it does](#-1-what-it-does)
2. [Assessment requirements checklist](#-2-assessment-requirements-checklist)
3. [Architecture](#-3-architecture)
4. [Tech stack](#-4-tech-stack)
5. [Data management](#-5-data-management)
6. [Analytics supported](#-6-analytics-supported)
7. [AI integration and safety](#-7-ai-integration-and-safety)
8. [Setup and execution](#-8-setup-and-execution)
9. [API reference](#-9-api-reference)
10. [Sample results](#-10-sample-results)
11. [Testing](#-11-testing)
12. [Error handling](#-12-error-handling)
13. [Known limitations](#-13-known-limitations)
14. [Future improvements](#-14-future-improvements)
15. [AI-assisted development](#-15-ai-assisted-development)
16. [Project structure](#-16-project-structure)

---

## 🎯 1. What it does

A business user types a question such as:

- What is the total revenue?
- Which product generated the highest revenue?
- Show me the monthly revenue trend.
- Which region generated the highest revenue?
- Compare revenue between January and February 2026.

The system works out **which analysis the user wants**, runs a **predefined, deterministic SQL query** on SQLite, and returns the answer together with the numbers that produced it.

The key design decision: **the AI only chooses *what* to compute, never *how* to query.** The LLM classifies the question into a known intent; it never writes or executes SQL. This keeps answers accurate and the database safe.

---

## ✅ 2. Assessment requirements checklist

| Requirement | How this project meets it | Section |
|---|---|---|
| **Data management:** load CSV into a database | Cleaned CSV is loaded into SQLite on startup | [5](#-5-data-management) |
| Handle missing or invalid records | Returned, zero-quantity and missing/zero-price rows are removed (51 → 48) | [5](#-5-data-management) |
| Explain how data is stored and queried | Schema and query approach documented | [5](#-5-data-management) |
| **Backend:** API accepting a question | FastAPI `POST /ask` | [9](#-9-api-reference) |
| Return a structured answer | JSON with `answer`, `intent`, `data`, `interpretation_method` | [9](#-9-api-reference) |
| Handle invalid requests and errors | Unsupported or empty questions return a clear, controlled response | [12](#-12-error-handling) |
| **Analytics:** at least 4 of 5 questions | **All 5** are supported | [6](#-6-analytics-supported) |
| Deterministic calculation | Predefined SQL on SQLite | [6](#-6-analytics-supported) |
| Display supporting figures | Every response includes a `data` object, shown in the UI | [9](#-9-api-reference) |
| **AI integration** | Groq LLM intent classification with rule-based fallback | [7](#-7-ai-integration-and-safety) |
| No destructive DB operations | LLM never produces SQL; only predefined read queries run | [7](#-7-ai-integration-and-safety) |
| Prevent unsupported/incorrect answers | Intent whitelist, deterministic SQL, fallback | [7](#-7-ai-integration-and-safety) |
| **User interface** | Streamlit app showing answer and supporting data | Live app |
| **Testing:** at least 5 tests | **15 Pytest tests passing** | [11](#-11-testing) |
| Document known limitations | Dedicated section | [13](#-13-known-limitations) |
| **Deliverables:** Git repo, README, architecture, tests | All included | This file |
| AI usage document | `docs/development_notes.md` | [15](#-15-ai-assisted-development) |

---

## 🏗️ 3. Architecture

```text
                    USER
                      |
                      v
        Natural-language question
                      |
                      v
            STREAMLIT FRONTEND
                      |   HTTP (POST /ask)
                      v
             FASTAPI BACKEND
                      |
                      v
            INTENT INTERPRETER
                      |
           +----------+----------+
           |                     |
           v                     v
      Groq LLM              Rule-based
      (optional)             fallback
           |                     |
           +----------+----------+
                      |
                      v
        Intent whitelist validation
        (unknown intent -> rejected)
                      |
                      v
         PREDEFINED SQL QUERIES
                      |
                      v
              SQLITE DATABASE
                      |
                      v
       Structured result (answer + data)
                      |
                      v
             STREAMLIT FRONTEND
```

### Request flow

1. The user enters a question in the Streamlit interface.
2. The frontend sends it to the FastAPI backend (`POST /ask`).
3. The intent interpreter classifies the question. It uses the Groq LLM when an API key is configured and falls back to rule-based matching otherwise.
4. The intent is validated against the list of supported intents.
5. The backend runs the predefined SQL query mapped to that intent.
6. SQLite returns the figures; the backend formats the answer and supporting data.
7. The frontend displays the answer and the figures behind it.

### Why this design

| Decision | Reason |
|---|---|
| LLM classifies intent only | Eliminates the risk of generated SQL being wrong or destructive |
| Predefined SQL per intent | Same question always gives the same, verifiable answer |
| Rule-based fallback | App works with no API key, no network, or an LLM outage |
| SQLite as source of truth | The LLM never calculates numbers, so it cannot hallucinate them |
| Separate frontend and backend | The API can be tested independently through Swagger UI |

---

## 🛠️ 4. Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,sqlite,pandas,github,vscode,git&theme=light" alt="Tech stack icons" />
</p>

| | Component | Technology |
|:-:|---|---|
| <img src="https://skillicons.dev/icons?i=python" width="32" /> | **Language** | Python |
| <img src="https://skillicons.dev/icons?i=pandas" width="32" /> | **Data processing** | Pandas |
| <img src="https://skillicons.dev/icons?i=sqlite" width="32" /> | **Database** | SQLite |
| <img src="https://skillicons.dev/icons?i=fastapi" width="32" /> | **Backend** | FastAPI (served with Uvicorn) |
| <img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="32" /> | **Frontend** | Streamlit |
| 🧠 | **LLM** | Groq API (optional) |
| 🧪 | **Testing** | Pytest |
| 📘 | **API exploration** | FastAPI Swagger UI (`/docs`) |
| <img src="https://skillicons.dev/icons?i=git" width="32" /> | **Version control** | Git and GitHub |

---|---|
| Language | Python |
| Data processing | Pandas |
| Database | SQLite |
| Backend | FastAPI (served with Uvicorn) |
| Frontend | Streamlit |
| LLM | Groq API (optional) |
| Testing | Pytest |
| API exploration | FastAPI Swagger UI (`/docs`) |

---

## 🗄️ 5. Data management

### Source data

`ai_bi_assistant_sales_data - GET.csv`: **51 transactions, 10 columns.**

| Column | Description |
|---|---|
| `Transaction_Id` | Unique transaction identifier |
| `Order_date` | Transaction date (`DD-MM-YYYY`) |
| `Product` | Product purchased |
| `Category` | Product category |
| `Region` | Sales region (North, South, East, West) |
| `Sales_channel` | Online or Retail |
| `Quantity` | Units purchased |
| `Unit_price` | Price per unit (₹) |
| `Discount_amount` | Transaction-level discount (₹) |
| `Status` | Completed or Returned |

### Cleaning rules

Three records in the source file are intentionally problematic. They are removed before loading:

| Transaction | Problem | Action |
|---|---|---|
| `TXN0033` | Status is `Returned` | Excluded (not a realised sale) |
| `TXN0034` | Quantity is `0` | Excluded (invalid quantity) |
| `TXN0051` | `Unit_price` is missing | Excluded (revenue cannot be calculated) |

**Result: 51 original records → 48 valid records loaded into SQLite.**

Dates are parsed as `DD-MM-YYYY` and stored in a consistent format so month grouping works correctly.

### How data is stored and queried

1. On startup the backend reads the CSV with Pandas, applies the cleaning rules, and writes the result to a SQLite table.
2. All analytics are plain SQL aggregations (`SUM`, `COUNT`, `GROUP BY`, `ORDER BY`) over that table.
3. The generated `sales.db` file is not committed; it is rebuilt from the CSV each time.

### Revenue formulas

```text
Gross Revenue = Quantity × Unit Price
Net Revenue   = Gross Revenue − Discount Amount
```

All "revenue" answers use **net revenue**. Discount is treated as a transaction-level amount, not per unit.

---

## 📈 6. Analytics supported

All five example questions from the brief are supported.

| Intent | Example question | What it returns |
|---|---|---|
| `total_revenue` | "What is the total revenue?" | Net revenue, gross revenue, total discount, transaction count |
| `top_product` | "Which product generated the highest revenue?" | Highest-earning product and its net revenue |
| `monthly_trend` | "Show me the monthly revenue trend" | Net revenue and transaction count for each month |
| `top_region` | "Which region generated the highest revenue?" | Highest-earning region and its net revenue |
| `revenue_comparison` | "Compare revenue between January and February 2026" | Revenue for both months, absolute change, percentage change |

Every response includes the supporting figures, not just a sentence, so users can verify the answer.

---

## 🛡️ 7. AI integration and safety

### How AI is used

The LLM (Groq) reads the user's question and returns **one intent label** from the supported list. It does not see the database and does not write SQL.

### How unsupported or incorrect answers are prevented

| Risk | Safeguard |
|---|---|
| LLM generates destructive SQL (`DROP`, `DELETE`, ...) | The LLM is never asked to generate SQL. Only predefined read-only queries exist. |
| LLM invents an intent | The returned label is checked against a whitelist; anything else is rejected |
| LLM invents numbers | Numbers come only from SQLite, never from the model |
| Question outside the supported scope | Returns a clear "unsupported question" response instead of a guess |
| LLM unavailable, rate-limited or no API key | Automatic fallback to rule-based interpretation |
| Not knowing which path answered | Response includes `interpretation_method` (`llm` or `rules`) |

### Optional Groq configuration

Without a key, the app runs entirely on the rule-based interpreter.

```env
GROQ_API_KEY=your_groq_api_key
```

- **Locally:** put it in a `.env` file or set it as an environment variable.
- **On Streamlit Cloud:** add it under the app's **Secrets** settings.
- **Never commit API keys or `.env` files to GitHub.**

---

## ⚙️ 8. Setup and execution

### Prerequisites

- Python 3.10 or newer
- Git

### 1. Clone the repository

```bash
git clone https://github.com/pavankumarchoudari/mini-ai-business-intelligence-assistant.git
cd mini-ai-business-intelligence-assistant
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. (Optional) Enable the LLM

```bash
# Windows PowerShell
$env:GROQ_API_KEY="your_groq_api_key"

# macOS / Linux
export GROQ_API_KEY="your_groq_api_key"
```

Skip this step to use the rule-based fallback.

### 5. Start the backend (Terminal 1)

```bash
python -m uvicorn backend.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

### 6. Start the frontend (Terminal 2)

Open a second terminal, activate the virtual environment, then run:

```bash
python -m streamlit run frontend/app.py
```

- App: http://localhost:8501

Keep the backend running while you use the frontend.

### 7. Run the tests

```bash
python -m pytest -v
```

---

## 🔌 9. API reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Backend health check |
| `GET` | `/data-quality` | Database initialisation and data-cleaning information |
| `POST` | `/ask` | Accepts a natural-language question and returns the analysis |

### Example request

```http
POST /ask
Content-Type: application/json
```

```json
{
  "question": "What is the total revenue?"
}
```

### Example response

```json
{
  "answer": "Total net revenue is ₹1,439,200.00.",
  "intent": "total_revenue",
  "data": {
    "total_revenue": 1439200,
    "gross_revenue": 1443700,
    "total_discount": 4500,
    "transaction_count": 48
  },
  "interpretation_method": "rules"
}
```

| Field | Meaning |
|---|---|
| `answer` | Human-readable answer |
| `intent` | The analytical operation that was run |
| `data` | The supporting figures behind the answer |
| `interpretation_method` | `llm` or `rules`, showing how the question was understood |

### Quick test with curl

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which region generated the highest revenue?"}'
```

---

## 📊 10. Sample results

These figures come from the cleaned dataset (48 records) and have been cross-checked against the source CSV.

| Question | Result |
|---|---|
| What is the total revenue? | ₹14,39,200 (gross ₹14,43,700, discounts ₹4,500) |
| Which product generated the highest revenue? | Monitor, ₹4,73,000 |
| Which region generated the highest revenue? | South, ₹4,11,200 |
| Compare January and February 2026 revenue | Up ₹24,350 (**+11.58%**) |

### Monthly revenue trend

| Month | Net revenue | Transactions |
|---|---:|---:|
| January 2026 | ₹2,10,250 | 8 |
| February 2026 | ₹2,34,600 | 8 |
| March 2026 | ₹2,23,900 | 8 |
| April 2026 | ₹2,40,700 | 8 |
| May 2026 | ₹3,18,500 | 8 |
| June 2026 | ₹2,11,250 | 8 |

---

## 🧪 11. Testing

Run from the project root:

```bash
python -m pytest -v
```

**Result: 15 tests passed.** The suite covers:

| Category | What is verified |
|---|---|
| **Valid questions** | Each supported analysis returns the expected figures |
| **Invalid questions** | Unsupported or unrelated questions are handled without crashing |
| **Edge cases** | Cleaning of returned, zero-quantity and missing-price records; month comparison logic |
| **Backend behaviour** | API responses and error handling |

The run reports three deprecation warnings that originate from underlying framework or testing libraries. They do not affect results.

---

## 🚨 12. Error handling

| Situation | Behaviour |
|---|---|
| Empty or malformed request | Rejected with a clear error response |
| Question not related to supported analytics | Controlled "unsupported question" message; no query is run |
| LLM service down or no API key | Falls back to rule-based interpretation |
| LLM returns an unknown intent | Rejected by whitelist validation |
| Invalid records in the source CSV | Removed during cleaning and counted (51 → 48) |

---

## ⚠️ 13. Known limitations

- Supports **five predefined intents**; questions outside them are not answered.
- Intent matching can misread unusual phrasing, especially in rule-based mode.
- Month comparison depends on the question naming two recognisable months.
- Revenue figures exclude returned transactions, so they represent net sales rather than all orders.
- The dataset is small (48 clean records), so results are suited to demonstration rather than statistical inference.
- Uses a local SQLite file with no authentication or multi-user support.
- No conversational memory: each question is handled independently.
- LLM mode requires a valid Groq API key and network access.
- The hosted demo runs on Streamlit Community Cloud's free tier, which may sleep after inactivity.

---

## 🔮 14. Future improvements

With another day of work:

1. **More intents and flexible parameters:** category, channel, product-level trends, custom date ranges.
2. **Charts:** line chart for the monthly trend, bar charts for product and region.
3. **Validated text-to-SQL:** let the LLM propose SQL, then enforce `SELECT`-only, allowed tables and columns, and a row limit before execution.
4. **Better classification:** structured LLM output with a confidence score and a clarifying question when confidence is low.
5. **Conversation context:** follow-ups such as "and for March?".
6. **Metrics:** average order value, growth rate, and profit if cost data is added.
7. **Deployment hardening:** Docker image, CI pipeline running Pytest on every push, and a production database.
8. **Exports:** downloadable summaries and reports.

---

## 🤝 15. AI-assisted development

AI coding assistants were used during development, as the assessment permits. The application logic, database operations and results were tested and verified independently of the AI tools.

AI assistance was used for:

- Planning the architecture and understanding how FastAPI, Streamlit and SQLite fit together
- Debugging implementation issues
- Improving API request and response handling
- Drafting test cases and documentation

The full record is in [`docs/development_notes.md`](docs/development_notes.md):

- Which AI tools were used
- How they were used
- Problems encountered
- How each was debugged
- What would be improved with another day of work

---

## 📁 16. Project structure

```text
mini-ai-business-intelligence-assistant/
├── backend/
│   └── main.py                 # FastAPI app, intent interpreter, SQL queries
├── frontend/
│   └── app.py                  # Streamlit interface
├── tests/                      # Pytest test suite (15 tests)
├── docs/
│   └── development_notes.md    # AI usage, problems, debugging, improvements
├── data/                       # Source sales CSV
├── requirements.txt
├── README.md
├── .gitignore
└── sales.db                    # Generated at runtime; not committed
```

---

## 🏁 Conclusion

The Mini AI Business Intelligence Assistant shows how natural language can sit on top of reliable analytics without sacrificing safety: the AI interprets the question, while deterministic SQL on a cleaned dataset produces every number. It covers all five example analyses, includes a fallback for when the LLM is unavailable, and is backed by automated tests and a live demo.

**Live app:** https://mini-ai-business-intelligence-assistant-nvnaicqz6kc8ruzzrnfote.streamlit.app/
