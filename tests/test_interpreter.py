from backend.ai_interpreter import deterministic_interpret

def test_total_revenue_intent():
    assert deterministic_interpret("What is the total revenue?")["intent"] == "total_revenue"

def test_top_product_intent():
    assert deterministic_interpret("Which product generated the highest revenue?")["intent"] == "top_product"

def test_monthly_trend_intent():
    assert deterministic_interpret("Show monthly revenue trend")["intent"] == "monthly_trend"

def test_month_comparison_intent():
    result = deterministic_interpret("Compare January 2026 and February 2026 revenue")
    assert result["intent"] == "revenue_comparison"
    assert result["month1"] == "2026-01"
    assert result["month2"] == "2026-02"

def test_unknown_question_is_not_guessed():
    assert deterministic_interpret("Tell me a joke") is None
