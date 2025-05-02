from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from ..models.payment import Payment

# Create a test client for the app
client = TestClient(app)


@pytest.fixture(scope='module')
def seeded_client():
    return client


def test_read_all_payments(seeded_client):
    response = seeded_client.get("/payments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0




def test_read_payment_by_id(seeded_client):
    response = seeded_client.get("/payments/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == {
        "user_id": 1,
        "promotion_id": 1,
        "amount": 12.6,
        "payment_id": 1,
        "created_at": "2025-05-01T21:19:21"
    }



def test_create_new_payment(seeded_client):
    payment_request = {
        "user_id": 1,
        "promotion_id": 1,
        "amount": 100.0
    }

    response = seeded_client.post("/payments/", json=payment_request)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "promotion_id" in data
    assert data["user_id"] == 1
    assert data["payment_id"] == 5
    assert data["amount"] == 100.0
    assert "created_at" in data




def test_update_existing_payment(seeded_client):
    payment_update = {
        "user_id": 1,
        "promotion_id": 2,
        "amount": 200.0
    }

    response = seeded_client.put("/payments/1", json=payment_update)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["user_id"] == 1
    assert data["promotion_id"] == 2
    assert data["payment_id"] == 1
    assert data["amount"] == 200.0
    assert "created_at" in data



def test_delete_payment(seeded_client):

    payment_request = {
        "user_id": 1,
        "promotion_id": 1,
        "amount": 100.0
    }

    response = seeded_client.post("/payments/", json=payment_request)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

    response = seeded_client.delete(f"/payments/{data['payment_id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["user_id"] == 1
    assert data["promotion_id"] == 1
    assert data["payment_id"] == 5
    assert data["amount"] == 100.0
    assert "created_at" in data

    response = seeded_client.get(f"/payments/{data['payment_id']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found"}




