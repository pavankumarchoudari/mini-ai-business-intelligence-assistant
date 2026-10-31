# Mini AI Business Intelligence Assistant

An AI-powered Business Intelligence application that allows users to analyze sales transaction data by asking questions in natural language. The application converts user questions into predefined analytical operations, retrieves accurate results from an SQLite database, and presents the insights through an interactive Streamlit interface.

## 1. Project Overview

The **Mini AI Business Intelligence Assistant** simplifies sales data analysis by allowing users to interact with business data using everyday language instead of writing SQL queries.

For example, users can ask:

- What is the total revenue?
- Which product generated the highest revenue?
- Show me the monthly revenue trend.
- Which region generated the highest revenue?
- Compare revenue between January and February 2026.

The system interprets the question, identifies the required analytical operation, executes predefined SQL queries against the SQLite database, and returns the result in a readable format.

The application uses an LLM-based intent classification approach with a rule-based fallback, making the system usable even when an LLM API key is not configured.

## 2. Objectives

- Make business data analysis accessible through natural language.
- Automate common sales analytics tasks.
- Retrieve accurate results using SQL and SQLite.
- Provide a simple and interactive dashboard.
- Use AI for understanding user questions without allowing uncontrolled SQL execution.
- Maintain reliable results through data cleaning, validation, and automated testing.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas |
| Database | SQLite |
| Backend | FastAPI |
| Frontend | Streamlit |
| AI / LLM Integration | Groq API (optional) |
| Testing | Pytest |
| API Testing | FastAPI Swagger UI |

## 4. Key Features

### 4.1 Natural Language Query Processing

Users can ask questions about sales data using normal English. The system identifies the user's analytical intent and maps it to a supported operation.

### 4.2 Sales Analytics

The application currently supports the following analytical operations:

- **Total Revenue:** Calculates total net revenue, gross revenue, and discounts.
- **Top Product:** Identifies the product generating the highest net revenue.
- **Monthly Revenue Trend:** Displays monthly revenue and transaction counts.
- **Top Region:** Identifies the region with the highest net revenue.
- **Revenue Comparison:** Compares revenue between two months and calculates the percentage change.

### 4.3 AI-Based Intent Classification

The application can use an LLM through the Groq API to classify natural-language questions into predefined analytical intents.

A rule-based fallback is also available when the API key is not configured or the AI service is unavailable.

### 4.4 Safe SQL Execution

The LLM is not allowed to generate and execute arbitrary SQL queries.

Instead, the application follows a controlled approach:

1. The user submits a natural-language question.
2. The system identifies the corresponding analytical intent.
3. The backend maps the intent to a predefined SQL operation.
4. The SQL query retrieves data from SQLite.
5. The result is returned to the frontend.

This approach helps prevent unsafe or unintended database operations.

### 4.5 Interactive User Interface

The Streamlit frontend allows users to enter questions and view the corresponding business insights and analytical results.

### 4.6 Data Quality Handling

The application processes the original sales dataset before loading it into the database. It handles invalid records such as returned transactions and transactions with invalid quantity or unit-price values.

### 4.7 Automated Testing

Pytest is used to validate the application's functionality and ensure that the supported analytical operations return expected results.

## 5. Dataset Description

The project uses a sales transaction dataset containing **51 original records and 10 columns**.

| Column | Description |
|---|---|
| Transaction_Id | Unique transaction identifier |
| Order_date | Date of the transaction |
| Product | Product purchased |
| Category | Product category |
| Region | Sales region |
| Sales_channel | Channel through which the sale occurred |
| Quantity | Number of units purchased |
| Unit_price | Price per unit |
| Discount_amount | Discount applied to the transaction |
| Status | Transaction status |

### Data Cleaning

The dataset is cleaned before being stored in SQLite.

The cleaning process includes:

- Removing returned transactions.
- Removing transactions with zero or invalid quantity.
- Removing transactions with zero or invalid unit price.
- Validating and preparing the transaction data for analysis.

After cleaning, **48 valid records** are loaded into the SQLite database.

### Revenue Calculation

The application uses the following calculations:

**Gross Revenue**

`Gross Revenue = Quantity × Unit Price`

**Net Revenue**

`Net Revenue = Gross Revenue − Discount Amount`

The discount amount is treated as a transaction-level discount.

## 6. System Architecture

The application follows a simple frontend-backend-database architecture.

```text
             USER
               |
               v
      Natural Language Question
               |
               v
       STREAMLIT FRONTEND
               |
               v
         FASTAPI BACKEND
               |
               v
       INTENT INTERPRETER
               |
        +------+------+
        |             |
        v             v
    Groq LLM      Rule-Based
    (Optional)     Fallback
        |             |
        +------+------+
               |
               v
       Predefined SQL Queries
               |
               v
         SQLITE DATABASE
               |
               v
       Analytical Results
               |
               v
       FASTAPI RESPONSE
               |
               v
       STREAMLIT FRONTEND
               |
               v
        BUSINESS INSIGHTS
```

### Workflow Explanation

1. The user enters a business-related question through the Streamlit interface.
2. The frontend sends the question to the FastAPI backend.
3. The intent interpreter identifies the type of analysis required.
4. The Groq LLM can classify the question when configured; otherwise, the rule-based interpreter is used.
5. The backend selects the corresponding predefined SQL query.
6. SQLite executes the query and retrieves the required information.
7. The backend formats the result and returns a structured response.
8. The frontend displays the answer and relevant analytical data.

## 7. Project Structure

```text
mini-ai-bi-assistant/
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── tests/
│
├── docs/
│   └── development_notes.md
│
├── data/
│
├── requirements.txt
├── README.md
├── .gitignore
└── sales.db              # Generated database; not committed
```

The SQLite database is initialized by the application using the cleaned sales data.

## 8. Installation and Setup

### Prerequisites

- Python installed
- Git
- Visual Studio Code or another code editor

### Step 1: Clone the Repository

```bash
git clone https://github.com/pavankumarchoudari/mini-ai-business-intelligence-assistant.git
```

Navigate into the project directory:

```bash
cd mini-ai-business-intelligence-assistant
```

### Step 2: Create a Virtual Environment

```bash
py -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## 9. Running the Application

The backend and frontend must run in separate terminals.

### Terminal 1: Start the FastAPI Backend

```bash
python -m uvicorn backend.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### Step 2: Access API Documentation

Open the following URL in your browser:

```text
http://127.0.0.1:8000/docs
```

FastAPI Swagger UI allows you to inspect and test the available API endpoints.

### Terminal 2: Start the Streamlit Frontend

Open another terminal, activate the virtual environment, and execute:

```bash
python -m streamlit run frontend/app.py
```

The frontend will be available at:

```text
http://localhost:8501
```

Keep the backend running while using the frontend.

## 10. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks backend health |
| GET | `/data-quality` | Returns database initialization and data information |
| POST | `/ask` | Accepts a natural-language question and returns analytical results |

### Example Request

**Endpoint:**

```text
POST /ask
```

**Request Body:**

```json
{
  "question": "What is the total revenue?"
}
```

### Example Response

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

The `interpretation_method` field indicates whether the question was interpreted using the rule-based approach or the configured AI-based approach.

## 11. Sample Analytical Results

The following results were obtained from the cleaned dataset during testing.

| User Question | Result |
|---|---|
| What is the total revenue? | ₹14,39,200 |
| Which product generated the highest revenue? | Monitor – ₹4,73,000 |
| Which region generated the highest revenue? | South – ₹4,11,200 |
| Compare January and February 2026 revenue. | Increased by ₹24,350 (11.58%) |

### Monthly Revenue Trend

| Month | Net Revenue |
|---|---:|
| January 2026 | ₹2,10,250 |
| February 2026 | ₹2,34,600 |
| March 2026 | ₹2,23,900 |
| April 2026 | ₹2,40,700 |
| May 2026 | ₹3,18,500 |
| June 2026 | ₹2,11,250 |

These values are calculated from the cleaned transaction records using the project's net revenue formula.

## 12. AI Integration and Safety

The project uses AI to understand natural-language questions and identify the required analytical operation.

The AI component is responsible for intent classification, not unrestricted database access.

For reliability and safety:

- Only supported analytical intents are accepted.
- The backend maps intents to predefined SQL queries.
- Arbitrary SQL generated by an LLM is not executed.
- A rule-based fallback is available when the AI service is unavailable.
- The database is used as the source of truth for analytical calculations.

### Optional Groq API Configuration

To enable AI-based intent classification, configure your Groq API key using the environment variable expected by the backend.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit API keys or `.env` files to GitHub.

The application can still perform supported analytics using its rule-based fallback without an API key.

## 13. Testing

The project uses Pytest for automated testing.

Run the test suite from the project root directory:

```bash
python -m pytest -v
```

### Test Results

**15 tests passed successfully.**

The tests validate the implemented application functionality, including supported analytical operations and backend behavior.

The test run also produced three deprecation warnings from underlying framework or testing-library APIs. These warnings did not cause test failures.

## 14. Challenges and Solutions

| Challenge | Solution |
|---|---|
| Converting natural-language questions into analytical operations | Implemented intent classification with a rule-based fallback |
| Maintaining accuracy in business calculations | Used predefined SQL queries and a consistent net revenue formula |
| Handling invalid transaction records | Added data cleaning and validation before database initialization |
| Connecting the frontend and backend | Integrated Streamlit with FastAPI endpoints |
| Preventing unsafe AI-generated SQL execution | Restricted database operations to predefined SQL queries |
| Validating application functionality | Implemented automated tests using Pytest |

## 15. Limitations and Future Enhancements

### Current Limitations

- The application currently supports five predefined analytical intents.
- Questions outside the supported analytical operations may not be answered.
- AI-based intent classification requires an appropriate Groq API configuration.
- The application currently uses a local SQLite database.
- The analytics are limited to the available fields in the provided sales dataset.

### Future Enhancements

- Support more complex natural-language analytical questions.
- Add additional business metrics such as profit, average order value, and sales growth.
- Introduce interactive charts and advanced visualizations.
- Support larger datasets and additional database systems.
- Add user authentication and role-based access.
- Improve intent classification and conversational context handling.
- Enable report generation and downloadable business summaries.

## 16. AI-Assisted Development

AI tools were used as development assistance during the implementation of this project.

The development process involved using AI assistance for:

- Understanding the project requirements and planning the application architecture.
- Understanding Python, FastAPI, Streamlit, and SQLite integration.
- Debugging implementation issues.
- Improving API request and response handling.
- Preparing test cases and documentation.

The application logic, database operations, data processing, and integration were tested to verify that the implemented features work as expected.

AI was used as an assistance tool, while database calculations and analytical results are produced by the application's backend logic.

For a detailed record of actual prompts, development decisions, debugging experiences, and solutions, refer to:

`docs/development_notes.md`

## 17. Repository

GitHub Repository:

https://github.com/pavankumarchoudari/mini-ai-business-intelligence-assistant

---

## Conclusion

The Mini AI Business Intelligence Assistant demonstrates how natural-language processing can simplify traditional business data analysis.

By combining Python, FastAPI, Streamlit, SQLite, and optional LLM-based intent classification, the application provides a simple and controlled way to retrieve meaningful insights from sales transaction data without requiring users to write SQL queries.

The project demonstrates practical implementation of backend development, database integration, data processing, AI-assisted intent interpretation, API testing, and application development.
