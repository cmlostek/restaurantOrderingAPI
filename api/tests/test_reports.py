import pytest
from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)

@pytest.fixture(scope='module')
def seeded_client():
    return client

def test_daily_revenue(seeded_client):
    response = seeded_client.get("/reports/revenue/2025-05-01")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "total_revenue" in data
    assert "sales_date" in data


