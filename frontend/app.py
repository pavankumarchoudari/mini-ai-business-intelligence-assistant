
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Add the project root to Python's import path.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.database import initialize_database
from backend.ai_interpreter import interpret_question
from backend.analytics import run_analytics


st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)


@st.cache_resource
def setup_database():
    return initialize_database()


st.title("📊 Mini AI Business Intelligence Assistant")
st.caption(
    "Ask questions about sales transactions in natural language. "
    "Answers are calculated from SQLite data."
)

# Initialize the SQLite database from the CSV file.
try:
    database_info = setup_database()
    st.sidebar.success("Database connected successfully")
    st.sidebar.metric("Loaded transactions", database_info["loaded_rows"])
except Exception as error:
    st.error(f"Database initialization failed: {error}")
    st.stop()


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
        st.write("• " + example)

    st.divider()
    st.caption(
        "Only supported business analytics questions are processed."
    )


st.subheader("Ask your business question")

with st.form("question_form"):
    question = st.text_input(
        "Enter your question",
        placeholder="Example: What is the total revenue?"
    )
    submitted = st.form_submit_button(
        "Analyze",
        type="primary"
    )


if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing your question..."):
            try:
                interpreted = interpret_question(question)

                if not interpreted:
                    st.warning(
                        "I could not understand that question. "
                        "Please try one of the supported examples."
                    )
                else:
                    result = run_analytics(
                        interpreted["intent"],
                        interpreted.get("month1"),
                        interpreted.get("month2")
                    )

                    st.success(result["answer"])

                    st.caption(
                        f"Detected intent: {result['intent']} | "
                        f"Interpretation method: "
                        f"{interpreted.get('method', 'unknown')}"
                    )

                    data = result.get("data")

                    if isinstance(data, dict):
                        st.subheader("Analysis details")
                        st.dataframe(
                            pd.DataFrame([data]),
                            use_container_width=True,
                            hide_index=True
                        )

                    elif isinstance(data, list):
                        st.subheader("Analysis details")
                        df = pd.DataFrame(data)

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                        if (
                            result["intent"] == "monthly_trend"
                            and not df.empty
                        ):
                            st.subheader("Monthly Revenue Trend")
                            chart_data = df.set_index("month")[
                                "net_revenue"
                            ]
                            st.bar_chart(chart_data)

            except ValueError as error:
                st.warning(str(error))
            except Exception as error:
                st.error(f"An error occurred: {error}")


st.divider()

with st.expander("Data Quality Information"):
    st.write("Information about the database initialization:")

    st.json(database_info)

    st.caption(
        "The database is initialized from the cleaned sales CSV file."
    )


st.caption(
    "Mini AI Business Intelligence Assistant | "
    "Python • Pandas • SQLite • Streamlit • FastAPI"
)
