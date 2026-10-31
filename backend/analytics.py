from .database import get_connection

SUPPORTED_INTENTS = {
    "total_revenue", "top_product", "monthly_trend",
    "top_region", "revenue_comparison"
}

def _rows(sql, params=()):
    with get_connection() as conn:
        conn.row_factory = __import__("sqlite3").Row
        return [dict(row) for row in conn.execute(sql, params).fetchall()]

def run_analytics(intent, month1=None, month2=None):
    """Execute only predefined, read-only analytics queries."""
    if intent not in SUPPORTED_INTENTS:
        raise ValueError("Unsupported question. Please ask about revenue, products, months, or regions.")

    if intent == "total_revenue":
        rows = _rows("""
            SELECT ROUND(COALESCE(SUM(Net_revenue), 0), 2) AS total_revenue,
                   ROUND(COALESCE(SUM(Gross_revenue), 0), 2) AS gross_revenue,
                   ROUND(COALESCE(SUM(Discount_amount), 0), 2) AS total_discount,
                   COUNT(*) AS transaction_count
            FROM sales
        """)
        r = rows[0]
        return {"answer": f"Total net revenue is ₹{r['total_revenue']:,.2f}.",
                "data": r, "intent": intent}

    if intent == "top_product":
        rows = _rows("""
            SELECT Product AS product,
                   ROUND(SUM(Net_revenue), 2) AS net_revenue,
                   SUM(Quantity) AS units_sold
            FROM sales GROUP BY Product
            ORDER BY net_revenue DESC, Product ASC LIMIT 1
        """)
        if not rows:
            return {"answer": "No sales data is available.", "data": [], "intent": intent}
        r = rows[0]
        return {"answer": f"{r['product']} generated the highest net revenue: ₹{r['net_revenue']:,.2f}.",
                "data": r, "intent": intent}

    if intent == "monthly_trend":
        rows = _rows("""
            SELECT substr(Order_date, 1, 7) AS month,
                   ROUND(SUM(Net_revenue), 2) AS net_revenue,
                   COUNT(*) AS transaction_count
            FROM sales GROUP BY substr(Order_date, 1, 7)
            ORDER BY month
        """)
        return {"answer": "Here is the monthly net revenue trend.",
                "data": rows, "intent": intent}

    if intent == "top_region":
        rows = _rows("""
            SELECT Region AS region,
                   ROUND(SUM(Net_revenue), 2) AS net_revenue,
                   SUM(Quantity) AS units_sold
            FROM sales GROUP BY Region
            ORDER BY net_revenue DESC, Region ASC LIMIT 1
        """)
        if not rows:
            return {"answer": "No sales data is available.", "data": [], "intent": intent}
        r = rows[0]
        return {"answer": f"{r['region']} generated the highest sales: ₹{r['net_revenue']:,.2f} net revenue.",
                "data": r, "intent": intent}

    if intent == "revenue_comparison":
        if not month1 or not month2:
            raise ValueError("Please provide two months, for example: Compare January 2026 and February 2026.")
        rows = _rows("""
            SELECT substr(Order_date, 1, 7) AS month,
                   ROUND(SUM(Net_revenue), 2) AS net_revenue
            FROM sales
            WHERE substr(Order_date, 1, 7) IN (?, ?)
            GROUP BY substr(Order_date, 1, 7)
        """, (month1, month2))
        values = {r["month"]: r["net_revenue"] for r in rows}
        if month1 not in values or month2 not in values:
            missing = [m for m in (month1, month2) if m not in values]
            raise ValueError(f"No completed valid sales found for: {', '.join(missing)}.")
        change = round(values[month2] - values[month1], 2)
        pct = round((change / values[month1]) * 100, 2) if values[month1] else None
        direction = "increased" if change > 0 else "decreased" if change < 0 else "did not change"
        return {
            "answer": f"Net revenue {direction} by ₹{abs(change):,.2f} from {month1} to {month2}."
                      + (f" ({abs(pct):.2f}%)." if pct is not None else ""),
            "data": {"month1": month1, "revenue1": values[month1],
                     "month2": month2, "revenue2": values[month2],
                     "change": change, "percentage_change": pct},
            "intent": intent
        }
