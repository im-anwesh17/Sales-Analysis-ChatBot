from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["database"] == "connected"
    print("Health Check Passed:", data)


def test_dashboard_overview():
    res = client.get("/api/v1/dashboard/overview")
    assert res.status_code == 200
    data = res.json()
    assert data["total_revenue"] > 0
    assert data["total_orders"] > 0
    print("Dashboard Overview Passed:", data)


def test_monthly_trend():
    res = client.get("/api/v1/dashboard/monthly-trend")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    print(f"Monthly Trend Passed: {len(data)} months returned.")


def test_rfm_analytics():
    res = client.get("/api/v1/analytics/rfm")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert "top_customers" in data
    print("RFM Analytics Passed:", len(data["summary"]), "segments.")


def test_chat_query():
    payload = {"question": "What were the top 5 selling products by revenue?"}
    res = client.post("/api/v1/chat/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "sql_query" in data
    assert "business_insight" in data
    assert "chart_config" in data
    assert len(data["rows"]) > 0
    print("Chat Query Passed!")
    print("Generated SQL:", data["sql_query"])
    print("Business Insight:", data["business_insight"])
    print("Chart Config:", data["chart_config"])


if __name__ == "__main__":
    print("--- Running Backend Integration Tests ---")
    test_health()
    test_dashboard_overview()
    test_monthly_trend()
    test_rfm_analytics()
    test_chat_query()
    print("--- ALL BACKEND TESTS PASSED SUCCESSFULLY! ---")
