import datetime

from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from ..models.promotion import Promotion

# Create a test client for the app
client = TestClient(app)


@pytest.fixture(scope='module')
def seeded_client():
    return client


def test_read_all_promotions(seeded_client):
    response = seeded_client.get("/promotions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert all("promotion_id" in promo and "code" in promo for promo in response.json())



def test_read_promotion_by_id(seeded_client):
    response = seeded_client.get("/promotions/1")
    assert response.status_code == 200
    assert response.json() ==  {
        "code": "SPRING10",
        "description": "10% off all dishes during the Spring season",
        "discount_percentage": 10,
        "valid_until": "2025-06-01T23:59:59",
        "promotion_id": 1
    }



def test_create_new_promotion(seeded_client):
    promotion_request = {
        "code": "TEST",
        "description": "This is a test promotion",
        "discount_percentage": 20,
        "valid_until": "2025-05-02T15:41:01.115Z"
    }

    response = seeded_client.post("/promotions/", json=promotion_request)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "TEST"
    assert data["description"] == "This is a test promotion"
    assert data["discount_percentage"] == 20
    assert "promotion_id" in data
    assert "valid_until" in data




def test_update_existing_promotion(seeded_client):
    promotion_update = {
        "code": "SPRING20",
        "description": "20% off all dishes during the Spring season",
        "discount_percentage": 20,
        "valid_until": "2025-06-01T23:59:59"
    }

    response = seeded_client.put("/promotions/1", json=promotion_update)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SPRING20"
    assert data["description"] == "20% off all dishes during the Spring season"
    assert data["discount_percentage"] == 20
    assert data["promotion_id"] == 1
    assert data["valid_until"] == "2025-06-01T23:59:59"


def test_delete_promotion(seeded_client):

    promotion_request = {
        "code": "TEST_DELETE",
        "description": "This is a test promotion to delete",
        "discount_percentage": 20,
        "valid_until": "2025-05-02T15:41:01.115Z"
    }

    response = seeded_client.post("/promotions/", json=promotion_request)
    assert response.status_code == 200
    promotion_id = response.json()["promotion_id"]
    assert promotion_id is not None


    response = seeded_client.delete("/promotions/5")
    assert response.status_code == 200
    data = response.json()

    assert data["code"] == "TEST_DELETE"
    assert data["description"] == "This is a test promotion to delete"
    assert data["discount_percentage"] == 20
    assert data["promotion_id"] == 5
    assert "valid_until" in data




