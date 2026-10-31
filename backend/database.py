from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sales_data.csv"
DB_PATH = ROOT / "sales.db"

REQUIRED_COLUMNS = [
    "Transaction_Id", "Order_date", "Product", "Category", "Region",
    "Sales_channel", "Quantity", "Unit_price", "Discount_amount", "Status"
]

def load_and_clean_csv(csv_path=DATA_PATH):
    """Load source CSV and return (clean_dataframe, exclusion_summary)."""
    df = pd.read_csv(csv_path)
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {missing_columns}")

    df = df[REQUIRED_COLUMNS].copy()
    original_count = len(df)

    df["Order_date"] = pd.to_datetime(
        df["Order_date"], format="%d-%m-%Y", errors="coerce"
    )
    for col in ["Quantity", "Unit_price", "Discount_amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Keep completed sales only; invalid records are excluded transparently.
    completed = df["Status"].astype(str).str.strip().str.lower().eq("completed")
    valid = (
        df["Transaction_Id"].notna()
        & df["Order_date"].notna()
        & df["Product"].notna()
        & df["Category"].notna()
        & df["Region"].notna()
        & df["Sales_channel"].notna()
        & df["Quantity"].notna()
        & df["Unit_price"].notna()
        & df["Discount_amount"].notna()
        & (df["Quantity"] > 0)
        & (df["Unit_price"] > 0)
        & (df["Discount_amount"] >= 0)
    )
    clean = df[completed & valid].copy()
    clean["Gross_revenue"] = clean["Quantity"] * clean["Unit_price"]
    clean["Net_revenue"] = clean["Gross_revenue"] - clean["Discount_amount"]
    clean["Order_date"] = clean["Order_date"].dt.strftime("%Y-%m-%d")

    summary = {
        "source_rows": int(original_count),
        "loaded_rows": int(len(clean)),
        "excluded_rows": int(original_count - len(clean)),
        "returned_rows": int((~completed).sum()),
        "invalid_or_incomplete_rows": int((completed & ~valid).sum()),
    }
    return clean, summary

def initialize_database(force_reload=False):
    """Create SQLite table and load cleaned CSV. Safe to call repeatedly."""
    if DB_PATH.exists() and not force_reload:
        with sqlite3.connect(DB_PATH) as conn:
            count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        if count:
            return {"database": str(DB_PATH), "loaded_rows": int(count), "already_initialized": True}

    df, summary = load_and_clean_csv()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DROP TABLE IF EXISTS sales")
        df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(Order_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(Product)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(Region)")
    return {"database": str(DB_PATH), **summary, "already_initialized": False}

def get_connection():
    return sqlite3.connect(DB_PATH)
