import os
import re
import json
from datetime import datetime

MONTHS = {
    "january":"01", "february":"02", "march":"03", "april":"04",
    "may":"05", "june":"06", "july":"07", "august":"08",
    "september":"09", "october":"10", "november":"11", "december":"12"
}

def _month_tokens(question):
    q = question.lower()
    found = []
    for name, number in MONTHS.items():
        if re.search(rf"\b{name}\b", q):
            year_match = re.search(rf"\b{name}\s+(20\d{{2}})\b", q)
            year = year_match.group(1) if year_match else "2026"
            found.append(f"{year}-{number}")
    return found

def deterministic_interpret(question):
    """Local fallback: maps common question wording to a supported intent."""
    q = question.lower().strip()
    months = _month_tokens(q)

    if any(x in q for x in ["compare", "difference", "change between", "between"]) and len(months) >= 2:
        return {"intent": "revenue_comparison", "month1": months[0], "month2": months[1], "method": "rules"}
    if "monthly" in q or "month-wise" in q or "month wise" in q or "trend" in q:
        return {"intent": "monthly_trend", "method": "rules"}
    if any(x in q for x in ["which product", "top product", "highest revenue product", "product generated"]):
        return {"intent": "top_product", "method": "rules"}
    if any(x in q for x in ["which region", "top region", "highest sales region", "region generated"]):
        return {"intent": "top_region", "method": "rules"}
    if any(x in q for x in ["total revenue", "revenue overall", "overall revenue", "how much revenue"]):
        return {"intent": "total_revenue", "method": "rules"}
    if len(months) >= 2 and any(x in q for x in ["revenue", "sales"]):
        return {"intent": "revenue_comparison", "month1": months[0], "month2": months[1], "method": "rules"}
    return None

def interpret_question(question):
    """Use Groq for natural-language intent classification when configured.
    The model never writes or executes SQL. Rules are the offline fallback.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            prompt = f"""
Classify this business analytics question into exactly one intent:
total_revenue, top_product, monthly_trend, top_region, revenue_comparison, unsupported.
For comparison, extract two months as YYYY-MM (assume 2026 if year omitted).
Return JSON only with keys intent, month1, month2. Use null when not applicable.
Question: {question}
"""
            response = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                messages=[{"role":"system","content":"You classify intent. Never calculate results or create SQL."},
                          {"role":"user","content":prompt}],
                temperature=0,
                response_format={"type":"json_object"},
                max_tokens=120
            )
            result = json.loads(response.choices[0].message.content)
            allowed = {"total_revenue", "top_product", "monthly_trend", "top_region", "revenue_comparison"}
            if result.get("intent") in allowed:
                return {"intent": result["intent"], "month1": result.get("month1"),
                        "month2": result.get("month2"), "method": "groq"}
            if result.get("intent") == "unsupported":
                return None
        except Exception:
            # A provider/network/key error must not break the core analytics.
            pass

    return deterministic_interpret(question)
