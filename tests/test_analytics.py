from backend.analytics import run_analytics

def test_total_revenue_returns_numeric_result():
    result = run_analytics("total_revenue")
    assert result["data"]["total_revenue"] > 0
    assert result["data"]["transaction_count"] > 0

def test_top_product_returns_product_and_revenue():
    result = run_analytics("top_product")
    assert result["data"]["product"]
    assert result["data"]["net_revenue"] > 0

def test_monthly_trend_has_six_months():
    result = run_analytics("monthly_trend")
    assert len(result["data"]) == 6
    assert result["data"][0]["month"] == "2026-01"

def test_top_region_returns_region():
    result = run_analytics("top_region")
    assert result["data"]["region"] in {"North", "South", "East", "West"}

def test_comparison_returns_change():
    result = run_analytics("revenue_comparison", "2026-01", "2026-02")
    assert "change" in result["data"]
    assert result["data"]["revenue1"] > 0

def test_unsupported_intent_is_rejected():
    import pytest
    with pytest.raises(ValueError):
        run_analytics("delete_all")
